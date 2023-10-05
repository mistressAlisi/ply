from django.contrib import admin, messages
from django.core.mail import send_mail

from event.models import Invoice, HotTable
from .models import Dealer, ArtistAlley, DealerAssistant, \
    TableDefinition, TableAssignment, TableSize
from registration.models import Event, RegistrantData
from import_export.admin import ImportExportModelAdmin
from django.utils import timezone
from django.core.mail import EmailMultiAlternatives
import uuid, datetime, pytz, urllib3, os, json
from django.core import mail
from django.http import HttpResponse

# Register your models here.

cur_event_pk = os.environ.get("UFLS_CURRENT_EVENT_PK")


def generate_manual_mailing(modeladmin, request, queryset):
    lst = ""
    for x in queryset:
        lst += x.account.username + ","
    return HttpResponse(lst)


generate_manual_mailing.short_description = "ADMIN - Generate a Manual Mailing List"


def lookup_registration_find_person(dataset, first_name, last_name):
    for x in dataset:
        if (x.conFirstName.lower() == first_name and x.conLastName.lower() == last_name):
            return x.displayId
    return False


def lookup_registration(modeladmin, request, queryset):
    http = urllib3.PoolManager()
    r = http.request('GET',
                     'https://backend.furrydelphia.org/api/v1/registrants-glimpse?event=%s' % (
                         3), headers={"Authorization": "Token %s" % (os.environ.get("UFLS_TOKEN"))})
    #incomingData = json.loads(r.data.decode('utf-8'))
    incomingData = RegistrantData.objects.filter(event_id=3)
    unable = ""
    for x in queryset:
        fn = x.first_name.lower()
        ln = x.last_name.lower()
        if (x.registered == False):
            lkp = lookup_registration_find_person(incomingData, fn, ln)
            if (lkp != False):
                x.registered = True
                x.registration_lookup = lkp
                # x.admin_notes = str(x.admin_notes) + "\\n" + x.status_sendalong_notes
                x.admin_notes = "%s \\n %s" % (x.admin_notes, x.status_sendalong_notes)
                x.status_sendalong_notes = "Verified your Registration using our automated system."
                x.save()
            else:
                unable = unable + "%s, " % (x.business_name)
    messages.success(request, "Action completed. Unable to process: " + unable)
    return True


lookup_registration.short_description = "ADMIN - Lookup registrations in UFLS"


def mass_mark_paid(modeladmin, request, queryset):
    for x in queryset:
        x.paid = True
        x.save()


mass_mark_paid.short_description = "PAYMENT - Mass Mark Paid"


def manual_place_account_into_match(modeladmin, request, queryset):
    for x in queryset:
        x.matchEmail = x.account.username
        x.save()


manual_place_account_into_match.short_description = "DEV - Set MatchEmail to Account E-mail"


def generate_table_invoice(modeladmin, request, queryset):
    current_event = Event.objects.filter(pk=cur_event_pk).first()
    for x in queryset:
        # first, check if paid
        dealer = x
        if dealer.paid == True:
            messages.info(request, "Dealer already has paid. No invoice generated.")
        # second, check if there's an invoice for this dealer that is paid and is a table invoice
        invoice = Invoice.objects.filter(user=dealer.account, invoice_type="table", paid=True).first()
        if invoice != None:
            if invoice.paid == True:
                messages.info(request, "Dealer already has a paid invoice. No invoice generated.")
        # third, check if there's already an active table invoice for this dealer.
        invoice = Invoice.objects.filter(user=dealer.account, invoice_type="table", paid=False).first()
        if invoice != None:
            messages.info(request, "Dealer already has an active invoice. No invoice generated.")
        else:
            # no invoice, we gotta make it ourselves.
            n = []
            if(x.upgr_flag):
                n = [
                    {
                        "name": "Table Backup Preference - Upgrade Only",
                        "percentage": "10.0"
                    },
                ]

            schema = {
                "item_map": ["l1"],
                "item_details": {
                    "l1": {
                        "title": "Table Registration (%s) for %s" % (dealer.table_size.name, dealer.business_name),
                        "price": dealer.table_size.toSquare()+'00',
                        "qty": "1",
                        "discounts": [],
                    },
                },
                "taxes": [["8.5", "PA Sales Tax"]],
                "discounts": n,
                "admin_notes": "Auto Generated Invoice",
            }

            eastern = pytz.timezone('US/Eastern')
            date_due = timezone.now()

            i = Invoice.objects.create(
                user=dealer.account,
                data=schema,
                invoice_type="table",
                description="Payment for Table for FD2023",
                date_due=date_due,
            )

            x.table_invoice = i.pk
            x.save()

            messages.success(request, "Invoice generated for Dealer.")


generate_table_invoice.short_description = "PAYMENT - Generate a Table Invoice"


def mark_as_approved(modeladmin, request, queryset):
    for x in queryset:
        x.status = "success"
        x.save()


mark_as_approved.short_description = "DECIDE - Mark as Approved (No Letter)"


def mark_as_under_review(modeladmin, request, queryset):
    for x in queryset:
        x.status = "primary"
        x.save()


mark_as_under_review.short_description = "DECIDE - Mark as Under Review (No Letter)"


def generate_slug(modeladmin, request, queryset):
    for x in queryset:
        x.save()


generate_slug.short_description = "DEV - Generate Table Slug Manually"


def mark_as_occupancy_limit(modeladmin, request, queryset):
    for x in queryset:
        x.status = "warning condition"
        x.save()


mark_as_occupancy_limit.short_description = "LEGACY - Mark as Occupancy Limited (No Letter)"


def mark_as_waitlisted(modeladmin, request, queryset):
    for x in queryset:
        x.status = "info"
        x.save()


mark_as_waitlisted.short_description = "DECIDE - Mark as Waitlisted (No Letter)"


def send_map_posted_notification(modeladmin, request, queryset):
    accepted = """
	Hello Furrydelphia Dealer!<br><br>

<p>We're reaching out to let you know that tables have been assigned for the upcoming convention. Please sign-in to the Dealers Dashboard and verify your Location on the Map.<br>
<br>If you have any questions or concerns, please let us know before August 1st, 2022.</p>
<hr>
<h4>Where can I find my table assignment?</h4>
<p>You can find your table assignment on <a href="https://dealers.furrydelphia.org/dashboard/">https://dealers.furrydelphia.org/dashboard/</a></p>
<h4>Is the Furrydelphia Dealers Den Map Live?</h4>
<p>Yes! The map is live at <a href="https://marketplace.furrydelphia.org/map">https://marketplace.furrydelphia.org/map</a></p>
<h4>Can I swap spots?</h4>
<p>Yes. If you would like to swap spots, please contact the dealer you'd like to swap spots with and have them and yourself contact marketplace@furrydelphia.org</p>
<hr>

Thank you, and we can’t wait to see you in August!<br><br>
<br>
- Yuukari, and the Furrydelphia Dealers Den Team &lt;3

	"""

    for x in queryset:
        if x.status == "success":
            letter_content = accepted
            send_mail("INFORMATION - %s - Dealers Den Map Posted" % (x.event.name), "HTML Message Content",
                      'Furrydelphia Marketplace Staff <bots@furrydelphia.org>', [x.account.username],
                      html_message=letter_content)

def send_confirmation_recieved(modeladmin, request, queryset):
    accepted = """
	Hello,<br><br>
	Someone (hopefully you) has applied to be in the Dealers Den for Furrydelphia 2023<br>
	This e-mail is to verify that we have recieved your application. Best of Luck!<br>
Best Wishes,<br>
Furrydelphia Marketplace Team<br>
Need Assistance? This e-mail is unmonitored. For questions and assistance, please e-mail marketplace@furrydelphia.org"""

    for x in queryset:
        send_mail("No Action Required - %s - Application Recieved" % (x.event.name), "HTML Message Content",
                  'Furrydelphia Marketplace Staff <bots@furrydelphia.org>', [x.account.username],
                  html_message=accepted)


send_map_posted_notification.short_description = "EMAIL - Send DD Map Post Notification"
send_confirmation_recieved.short_description = "EMAIL - Send Confirmation of Application"


def send_packet_notice(modeladmin, request, queryset):
    accepted = """
	Hello Furrydelphia Dealer!<br><br>

<p>We're reaching out to let you know that the dealers information packet is now available. Please sign-in to the Dealers Dashboard to review.<br>
<br>If you have any questions or concerns, please let us know before con.</p>
<hr>
<h4>Where can I find the Dealer Packet?</h4>
<p>Sign in to the dashboard at <a href="https://dealers.furrydelphia.org/dashboard/">https://dealers.furrydelphia.org/dashboard/</a> and click 'Your Dealers Packet' under 'Dealers Information'</p>
<hr>

Thank you, and we can’t wait to see you in August!<br><br>
<br>
- Fawkes, and the Furrydelphia Dealers Den Team &lt;3

	"""

    for x in queryset:
        if x.status == "success":
            letter_content = accepted
            send_mail("INFORMATION - %s - Dealer Packet Available" % (x.event.name), "HTML Message Content",
                      'Furrydelphia Marketplace Staff <bots@furrydelphia.org>', [x.account.username],
                      html_message=letter_content)


send_packet_notice.short_description = "EMAIL - Send DD Packet Notice"


def send_decision_letters(modeladmin, request, queryset):


    for x in queryset:

        accepted = """
        	Good morning Furrydelphia Dealers Den Applicant,<br><br>

        We’re reaching out to let you know that you have been accepted to the Furrydelphia 2023 Dealers Den! <br>

        <h4>Immediate Next Steps for You</h4>

        <br>
        <br>
        <p><b>You have been assigned the following table size: %s</b></p>
        <p><em>If your table size is different from your preferred size, you were given your alternative size to be fit into the Den layout.</em></p>
        <br>
        <ol>
            <li>Pay for your table in the Furrydelphia App by no later than April 14th, 2023 Your invoice will appear in the Furrydelphia App.</li>
            <li>Register for Furrydelphia in the Furrydelphia App once Paid</li>
            <li>Ensure your PA Sales Tax ID is current, up-to-date, and established with your provided Name, Address, and Business Name.</li>
            <li>Review your Dealers Packet in the Dealers Dashboard of the Furrydelphia App</li>
            <li>Keep an eye out in April for our Hotel Room Block opening e-mail</li>
        </ol>
        <hr>

        <h4>Regarding Your Sales Tax License</h4>
        <p><em>A <b>valid</b> Sales Tax License is required to vend at any convention in Pennsylvania.</em> If you are a new business, or from out of state, you can begin the process of obtaining a PA Sales Tax License at: <a href="https://mypath.pa.gov">https://mypath.pa.gov</a></p>

        <h5>What is a valid PA Sales Tax License?</h5>
        <p>A valid PA Sales Tax License is a license that has not been revoked due to expiry, deliquency, or any other reason PA might revoke your Sales Tax License. To check if your license is valid, please use PA's tool at: <a href="https://data.pa.gov/Licenses-Certificates/Sales-Use-Hotel-Occupancy-Tax-Licenses-and-Certifi/ugeq-ckxd">https://data.pa.gov/Licenses-Certificates/Sales-Use-Hotel-Occupancy-Tax-Licenses-and-Certifi/ugeq-ckxd</a>

        <hr>

        <h4>Other, very important things to keep in mind</h4>
        <ol>
        <li>Tables must be paid in full by April 14th, 2023. Please go to <a href='https://app.furrydelphia.org/marketplace'>https://app.furrydelphia.org/marketplace</a> and log in with your credentials to complete this process. If you forgot and need to reset your password, you can do that from the Login Screen.</li>

        <li>Your table price includes one complimentary registration, as well as a daily lunch for Friday, Saturday, and Sunday of the con. We appreciate you all providing your feedback on your dietary restrictions, and will do our absolute best to accommodate you!</li>

        <li>You can also register your assistants and yourselves using the codes available to you once you pay for your table. Please do so at your earliest convenience!</li>

        <li>Your code will activate your complimentary base registration. Your Assistant Codes will activate a discount on the base registration for your assistants. <b>At Con, you will pick up your badge at Con Store.</b></li>

        <li><em>Tax Licenses should be entered into the Dealers Den System no later than May 14th, 2023.</em></li>

        <li><em>Our Dealers Den Vendor Block will open on April 14th, 2023. Once you've paid for your space, You can access it from the Dealers Dashboard in the Furrydelphia App.</em></li>
        </ol>
        <hr>

        Thank you, and we can’t wait to see you in August!<br><br>
        <br>
        - Fawkes, and the Furrydelphia Dealers Den Team &lt;3

        	""" % (str(x.table_size))

        tentative = """
        	Good morning Furrydelphia Dealers Den Applicant,<br>

        We’re reaching out to let you know that you have unfortunately not been accepted to the Furrydelphia 2023 Dealers Den in our first pass of approvals.<br><br>

        Please note that you have been automatically added to our waitlist and will be contacted if a spot opens up. This is not an uncommon occurrence, especially the closer we get to the convention, so we suggest keeping an eye on your emails for further communications from us! <br><br>

        If you’d like, you can also apply for our Artist Alley by going to <a href='https://app.furrydelphia.org/marketplace'>https://app.furrydelphia.org/marketplace</a><br><br>

        Thank you!<br><br>
        <br>
        - Fawkes, and the Furrydelphia Dealers Den Team 

        	"""

        if x.status == "info":
            letter_content = tentative
            send_mail("No Action Required - %s - Application Waitlisted" % (x.event.name), "HTML Message Content",
                      'Furrydelphia Marketplace Staff <bots@furrydelphia.org>', [x.account.username],
                      html_message=letter_content)
        if x.status == "success":
            letter_content = accepted
            send_mail("ACTION REQUIRED - %s - Application Accepted" % (x.event.name), "HTML Message Content",
                      'Furrydelphia Marketplace Staff <bots@furrydelphia.org>', [x.account.username],
                      html_message=letter_content)


send_decision_letters.short_description = "DECIDE - Send Decision Letters"


def payment_reminder(modeladmin, request, queryset):
    current_event = Event.objects.filter(pk=3).first()
    dealers = []
    for x in queryset:
        if x.paid == False:
            if x.status == "success" or x.status == "success hello" or x.status == "warning condition":
                dealers.append(x.account.username)
    letter = """
	Dear Furrydelphia Dealers Den Applicant,<br><br>

	<p>We're sending you this courtesy message that your table is currently recorded as Unpaid in our system. A gentle reminder that payment for Dealers Den Tables are due by April 14th, 2023. If by April 14th, 2023 your table is unpaid you must reach out to us to request a payment extension.</p>
	<h4>What can I do?</h4>
	<ol>
		<li>Login to the Furrydelphia Marketplace Dashboard at <a href="https://app.furrydelphia.org/marketplace">https://app.furrydelphia.org/marketplace</a>.</li>
		<li>Follow the on-screen instructions and fill out the Square Payment Form.</li>
	</ol>
	<h4>Are you offering payment extensions?</h4>
	<p>Unfortunatly, due to the nature of our convention we are unable to offer payment extensions beyond May 15th, 2023. This is on account of our revenue owed to the hotel during this period, as well as fairness to the applicants on the Waitlist. Due to this hard deadline, we are frequently sending out messages like this one to dealers to keep in constant communication.</p>
	<h4>My Tax License is not Confirmed yet, should I still pay for my table?</h4>
	<p>Yes. We will work with dealers who have paid for their table but have not yet recieved confirmation for their tax license due to the PA Department of Revenue's current status.</p>
	<h4>How do you know my table is not paid for?</h4>
	<p>This is an automated message that automatically checks the Marketplace System for all unpaid tables. If you believe you are recieving this in error, please e-mail marketplace@furrydelphia.org for assistance.</p>
<hr>
<p>Please make sure you check your Furrydelphia Marketplace Dashboard for any further activities you must complete before the convention starts in August. Any actions you still need to accomplish will be listed under your Approval at <a href="https://app.furrydelphia.org/marketplace">https://app.furrydelphia.org/marketplace</a><br><br>

Thanks,</p>
<br>
- Yuukari, and the Furrydelphia Dealers Den Team &lt;3<br><br>Need Assistance? This e-mail is unmonitored. For questions and assistance, please e-mail marketplace@furrydelphia.org

	"""

    with mail.get_connection() as connection:
        email = EmailMultiAlternatives(
            subject="ACTION REQUIRED - %s - Dealers Den Table Payment Reminder" % (current_event.name),
            body="HTML Message Content",
            from_email="Furrydelphia Marketplace Staff <bots@furrydelphia.org>",
            bcc=dealers,
            to=["marketplace@furrydelphia.org"],
            reply_to=["marketplace@furrydelphia.org"],
            connection=connection,
        )
        email.attach_alternative(letter, "text/html")
        email.send()


payment_reminder.short_description = "REMINDER - Send Payment Reminders to Unpaid Dealers"


def hotel_block(modeladmin, request, queryset):
    current_event = Event.objects.filter(pk=cur_event_pk).first()
    dealers = []
    for x in queryset:
        if (x.account.username == "yuu"):
            dealers.append(x.matchEmail)
        else:
            dealers.append(x.account.username)
    letter = """
	Dear Furrydelphia Dealer,<br><br>

	<p>We're happy to announce that this year's room block for Vendors is now officially open. If you have paid for your table, you now have access to the booking portal online.</p>
	<h4>What can I do?</h4>
	<ol>
		<li>Login to the Furrydelphia Marketplace Dashboard at <a href="https://dealers.furrydelphia.org/dashboard/">https://dealers.furrydelphia.org/dashboard/</a>.</li>
		<li>Under "Your Actions" select "3. Access Room Block"</li>
		<li>Follow the on-screen instructions.</li>
	</ol>
	<h4>I haven't logged in yet to this year's Dashboard yet.</h4>
	<p>If you haven't logged in yet, please follow the instructions sent to you in a previous e-mail to login and get started.</p>
<hr>
<p>Please make sure you check your Furrydelphia Marketplace Dashboard for any further activities you must complete before the convention starts in August. Any actions you still need to accomplish will be listed under your Approval at <a href="https://dealers.furrydelphia.org/dashboard/">https://dealers.furrydelphia.org/dashboard/</a><br><br>

Thanks, and stay Safe!</p>
<br>
- Yuukari, and the Furrydelphia Dealers Den Team &lt;3<br><br>Need Assistance? This e-mail is unmonitored. For questions and assistance, please e-mail marketplace@furrydelphia.org

	"""

    with mail.get_connection() as connection:
        email = EmailMultiAlternatives(
            subject="ACTION REQUIRED - %s - REMINDER! Hotel Room Block Open" % (current_event.name),
            body="HTML Message Content",
            from_email="Furrydelphia Marketplace Staff <bots@furrydelphia.org>",
            bcc=dealers,
            to=["marketplace@furrydelphia.org"],
            reply_to=["marketplace@furrydelphia.org"],
            connection=connection,
        )
        email.attach_alternative(letter, "text/html")
        email.send()


hotel_block.short_description = "EMAIL - Send Hotel Block Open Message"


def dealer_hotel_reminder(modeladmin, request, queryset):
    current_event = Event.objects.filter(pk=cur_event_pk).first()
    dealers = []
    for x in queryset:
        dealers.append(x.matchEmail)
    letter = """

	Dear Furrydelphia Dealer,<br><br>

	<p>We're happy to announce that this year's room block for Vendors is now officially open. If you have paid for your table, you have access to the booking portal online.</p>
	<p><em>Rooms will fill up fast in the vendors block! Please get your reservations in ASAP!</em></p>
	<h4>What can I do?</h4>
	<ol>
		<li>Login to the Furrydelphia Marketplace Dashboard at <a href="https://dealers.furrydelphia.org/dashboard/">https://dealers.furrydelphia.org/dashboard/</a>.</li>
		<li>Under "Your Actions" select "3. Access Room Block"</li>
		<li>Follow the on-screen instructions.</li>
	</ol>
	<h4>I haven't logged in yet to this year's Dashboard yet.</h4>
	<p>If you haven't logged in yet, please follow the instructions sent to you in a previous e-mail to login and get started.</p>
<hr>
<p>Please make sure you check your Furrydelphia Marketplace Dashboard for any further activities you must complete before the convention starts in August. Any actions you still need to accomplish will be listed under your Approval at <a href="https://dealers.furrydelphia.org/dashboard/">https://dealers.furrydelphia.org/dashboard/</a><br><br>

Thanks, and stay Safe!</p>
<br>
- Yuukari, and the Furrydelphia Dealers Den Team &lt;3<br><br>Need Assistance? This e-mail is unmonitored. For questions and assistance, please e-mail marketplace@furrydelphia.org

	"""

    with mail.get_connection() as connection:
        email = EmailMultiAlternatives(
            subject="ACTION REQUIRED - %s - Vendor Hotel Block Open!" % (current_event.name),
            body="HTML Message Content",
            from_email="Furrydelphia Marketplace Staff <bots@furrydelphia.org>",
            bcc=dealers,
            to=["marketplace@furrydelphia.org"],
            reply_to=["marketplace@furrydelphia.org"],
            connection=connection,
        )
        email.attach_alternative(letter, "text/html")
        email.send()


dealer_hotel_reminder.short_description = "REMINDER - Send Hotel Reminder E-mail (2022)"


def dealer_registration_reminder(modeladmin, request, queryset):
    current_event = Event.objects.filter(pk=cur_event_pk).first()
    dealers = []
    for x in queryset:
        dealers.append(x.matchEmail)
    letter = """

	Dear Furrydelphia Dealer,<br><br>

	<p>Our records indicate that you have paid for your table, but you have not yet registered for the convention. Please note that Furrydelphia Registration is required in order to pick up your table at the convention!</p>
	<p>There is no specific deadline for this to occur, but we do recommend you register before the convention so you can quickly pick up your table on Thursday or Friday.</p>
	<h4>What can I do?</h4>
	<ol>
		<li>Login to the Furrydelphia Marketplace Dashboard at <a href="https://dealers.furrydelphia.org/dashboard/">https://dealers.furrydelphia.org/dashboard/</a>.</li>
		<li>Under "Your Actions" select "2. Register for Furrydelphia"</li>
		<li>Follow the on-screen instructions.</li>
	</ol>
	<h4>I've already registered, why is the system saying I am not registered?</h4>
	<p>We check your registration using your First and Last Name provided to us during the application process. If you have entered a different name from the name you gave us when you applied for Dealers, please reach out to us at: marketplace@furrydelphia.org</p>
	<p>Note: We do not automatically check registrations for Assistants, so please make sure your assistants are registered as well!</p>
<hr>
<p>Please make sure you check your Furrydelphia Marketplace Dashboard for any further activities you must complete before the convention starts in August. Any actions you still need to accomplish will be listed under your Approval at <a href="https://dealers.furrydelphia.org/dashboard/">https://dealers.furrydelphia.org/dashboard/</a><br><br>

Thanks, and stay Safe!</p>
<br>
- Yuukari, and the Furrydelphia Dealers Den Team &lt;3<br><br>Need Assistance? This e-mail is unmonitored. For questions and assistance, please e-mail marketplace@furrydelphia.org

	"""

    with mail.get_connection() as connection:
        email = EmailMultiAlternatives(
            subject="ACTION REQUIRED - %s - Register for Furrydelphia!" % (current_event.name),
            body="HTML Message Content",
            from_email="Furrydelphia Marketplace Staff <bots@furrydelphia.org>",
            bcc=dealers,
            to=["marketplace@furrydelphia.org"],
            reply_to=["marketplace@furrydelphia.org"],
            connection=connection,
        )
        email.attach_alternative(letter, "text/html")
        email.send()


dealer_registration_reminder.short_description = "REMINDER - Send Registration Reminder"


def approve_license(modeladmin, request, queryset):
    current_event = Event.objects.filter(pk=cur_event_pk).first()

    letter = """
	Good morning Furrydelphia Dealers Den Applicant,<br><br>

We’re reaching out to let you know that your PA Tax License has been verified against the current Sales, Use & Hotel Occupancy Tax Licenses and Certificates Current Monthly County Revenue dataset from the Pennsylvania Department of Revenue.<br>

Please make sure you check your Furrydelphia Marketplace Dashboard for any further activities you must complete before the convention starts in August. Any actions you still need to accomplish will be listed under your Approval at <a href="https://app.furrydelphia.org/marketplace">https://app.furrydelphia.org/marketplace</a><br><br>

Thanks!<br>

<br>
- Fawkes, and the Furrydelphia Dealers Den Team &lt;3<br><br>Need Assistance? This e-mail is unmonitored. For questions and assistance, please e-mail marketplace@furrydelphia.org

    """

    for x in queryset:
        x.license_verified = True
        x.save()
        letter_content = letter
        send_mail("No Action Required - %s - PA Tax License Approved" % (x.event.name), "HTML Message Content", 'Furrydelphia Marketplace Staff <bots@furrydelphia.org>', [x.account.username], html_message=letter_content)


approve_license.short_description = "ADMIN - Approve License and Send E-mail"


def license_warning(modeladmin, request, queryset):
    current_event = Event.objects.filter(pk=cur_event_pk).first()

    letter = """
	<p>Good Afternoon Furrydelphia Dealer,</p>

<p>Please read the following information carefully.</p>

<p>If you are receiving this message, we do not have a valid tax license on file for you or could not validate that your license number provided is correct.</p>

<h3>I already have put a tax license in the system. Why am I getting this e-mail?</h3>
<p>If you are receiving this message, the number entered did not return a valid business. We also searched all businesses by Trade Name, Legal Name, and Address.<br></p>
<br>
<h3>I would rather wait until I am accepted to apply for a license. Is that ok?</h3>
<p>At the present time, licenses are generally approved within 1-2 weeks of application. However, The verification system may be behind by 3-5 weeks. If we can't verify your tax license by the due date, we may have to take action to ensure that all dealers are valid in our den, including a request to see and keep a physical copy of your PA Sales Tax License.</p>
<br>
<h3>What can I do?</h3>
<ul>
	<li>Please verify that your license is up to date. Instructions are available in the Furrydelphia App on what to do next.</li>
	<li>Double check that you've provided an accurate address, name, and trade name to match up to your PA License Registration.</li>
	<li>Your license <em>must</em> be with the Pennsylvania Department of Revenue. We do not accept Federal or Out-Of-State Tax Licenses, even for organizations based outside of Pennsylvania.</li>
	<li>A gentle reminder that you must have a valid license within 60 days of acceptance to the Dealers Den in order to keep your spot. If by 60 days you do not have a valid license we will be forced to waitlist you and select another applicant.</li>
</ul>
<br>
<p>The deadline for having an accurate PA License in your account was April 14th, 2023.</p>
<h3>What if I have yet to apply for a License?</h3>
<p>We highly recommend applying for a PA Sales Tax License immediately. To apply, follow the instructions in the Furrydelphia App. If you have applied for a tax license, have been approved, and are still seeing this e-mail please reach out to me at yuukari@furrydelphia.org.</p>
<h3>How can I know my license was verified?</h3>
<p>You will receive an e-mail from Marketplace Staff stating your tax license was verified successfully.</p>
<h3>How do you know my license isn't verified? Where can I check?</h3>
<p>We use the PA Database for Sales, Use & Hotel Occupancy Tax Licenses and Certificates Current Monthly County Revenue published by the Pennsylvania Department of Revenue on the OpenDataPA Website.<br>You can view this table for yourself at this link: <a href="https://data.pa.gov/Licenses-Certificates/Sales-Use-Hotel-Occupancy-Tax-Licenses-and-Certifi/ugeq-ckxd">https://data.pa.gov/Licenses-Certificates/Sales-Use-Hotel-Occupancy-Tax-Licenses-and-Certifi/ugeq-ckxd</a><br><br><em>If you have applied for a tax license, have been approved, and are still seeing this e-mail please reach out to me at yuukari@furrydelphia.org.</em></p>
<h3>What happens if my License isnt verified before the due date?</h3>
<p>You will receive this reminder e-mail as well as communications directly from us until we work out a plan on how to get your license verified. If we don't hear from you within 60 days of initial acceptance, you will be waitlisted.</p>
<br><br>
<p>Thank you for your attention, and we hope to hear from you soon.</p>
<p>-Yuukari and the Furrydelphia Marketplace Team</p>

<br><br>Need Assistance? This e-mail is unmonitored. For questions and assistance, please e-mail marketplace@furrydelphia.org

	"""

    for x in queryset:
        letter_content = letter
        send_mail("ACTION REQUIRED - %s - PA Tax License Information Required" % (x.event.name), "HTML Message Content",
                  'Furrydelphia Marketplace Staff <bots@furrydelphia.org>', [x.account.username],
                  html_message=letter_content)


license_warning.short_description = "ADMIN - Send a License Warning E-mail"


def resend_verification_email(modeladmin, request, queryset):
    current_event = Event.objects.filter(pk=cur_event_pk).first()
    for x in queryset:
        px = x
        v = x.getVerifyRecord()
        t = """
Hello,
	Someone (hopefully you) has applied to be a Dealer for %s.
	If this was you, awesome! We just need you to verify your e-mail so we can make sure it is you.
	To verify your e-mail, click below:
	https://dealers.furrydelphia.org/verify/%s/
	If this was not you, please disregard this e-mail.

Best Wishes,
Furrydelphia Marketplace Team

Need Assistance? This e-mail is unmonitored. For questions and assistance, please e-mail marketplace@furrydelphia.org
			""" % (px.event.name, v.key)
        send_mail("ACTION REQUIRED - %s - Verify E-mail for Application Submission" % (px.event.name), t,
                  'Furrydelphia Marketplace Staff <bots@furrydelphia.org>', [x.account.username])


resend_verification_email.short_description = "DEV - Resend E-mail Verification"


def send_reset_email(modeladmin, request, queryset):
    current_event = Event.objects.filter(pk=cur_event_pk).first()
    for x in queryset:
        x.sendResetLink()


send_reset_email.short_description = "DEV - Send Reset E-mail"


class DealerAssistantInline(admin.TabularInline):
    model = DealerAssistant
    extra = 1


class DealerAdmin(ImportExportModelAdmin):
    list_display = ['business_name', 'license_verified', 'contract_signed', 'paid', 'registered', 'account', 'status',
                    'license', 'table_size', 'upgr_flag', 'area', 'first_name', 'last_name', 'type_of_wares', 'matchEmail']
    list_filter = ['event', 'status', 'license_verified', 'paid', 'registered', 'table_size', 'type_of_wares', 'area',
                   'contract_signed']
    list_editable = ['license_verified', 'contract_signed', 'paid', 'registered', 'status']
    actions = [resend_verification_email, send_decision_letters,
               manual_place_account_into_match, mark_as_approved, mark_as_under_review, mark_as_waitlisted,
               generate_table_invoice, approve_license, license_warning, generate_slug, payment_reminder,
               generate_manual_mailing, mass_mark_paid, mark_as_occupancy_limit, dealer_hotel_reminder, hotel_block,
               lookup_registration, dealer_registration_reminder, send_map_posted_notification, send_packet_notice, send_confirmation_recieved]
    readonly_fields = ['allowedAssistants', 'remainingAssistants']
    inlines = [DealerAssistantInline]


class ResetPwKeyAdmin(admin.ModelAdmin):
    list_display = ['account', 'used']
    actions = [send_reset_email]


class TableSizeAdmin(ImportExportModelAdmin):
    pass


def aa_generate_manual_mailing(modeladmin, request, queryset):
    lst = ""
    for x in queryset:
        lst += x.email + ","
    return HttpResponse(lst)


aa_generate_manual_mailing.short_description = "AA Generate a Manual Mailing List"


def aa_send_space_reservation(modeladmin, request, queryset):
    current_event = Event.objects.filter(pk=cur_event_pk).first()
    for x in queryset:
        px = x
        t = """
Hello,<br><br>
	Thank you for registering for this years Artist Alley! Your assigned day is <b>%s</b>.<br><br>Please show up to the Dealers Den Con Store by 9am on your assigned day to claim your space and pay the table fee. You will also recieve instructions for the artist alley at that time. Please note that if you do not show by 10am your space reservation will be forfitted to the next first-come person.<br><br>Any questions, please let us know. We look forward to seeing you in August!

Best Wishes,<br>
Amaretto, Fawkes, Sandie, and the Furrydelphia Marketplace Team
<hr>
Need Assistance? This e-mail is unmonitored. For questions and assistance, please e-mail marketplace@furrydelphia.org
			""" % (x.get_assigned_day_display())
        send_mail("NO ACTION REQUIRED - %s - Artist Alley Assigned Day" % (px.event.name), "Please Enable HTML Messages",
                  'Furrydelphia Marketplace Staff <bots@furrydelphia.org>', [x.email], html_message=t)


aa_send_space_reservation.short_description = "AA Send Space Reservation"


def aa_send_waitlist(modeladmin, request, queryset):
    current_event = Event.objects.filter(pk=cur_event_pk).first()
    for x in queryset:
        px = x
        t = """
Hello,<br><br>
	Thank you for registering for this years Artist Alley! Due to the popularity of your requested day(s) you have been placed on the Waitlist. We highly suggest you show up bright and early by 10AM on your requested day(s) as any reservation that does not show up by that time will have their reservation forfit.<br>Any questions, please let us know!<br><br>

Best Wishes,<br>
Amaretto, Fawkes, Sandie, and the Furrydelphia Marketplace Team
<hr>
Need Assistance? This e-mail is unmonitored. For questions and assistance, please e-mail marketplace@furrydelphia.org
			"""
        send_mail("NO ACTION REQUIRED - %s - Artist Alley Assigned Day" % (px.event.name), "Please Enable HTML Messages",
                  'Furrydelphia Marketplace Staff <bots@furrydelphia.org>', [x.email], html_message=t)


aa_send_waitlist.short_description = "AA Send Waitlist"


def aa_assign_friday(modeladmin, request, queryset):
    for x in queryset:
        x.assigned_day = "friday"
        x.save()


aa_assign_friday.short_description = "Assign Friday"


def aa_assign_saturday(modeladmin, request, queryset):
    for x in queryset:
        x.assigned_day = "saturday"
        x.save()


aa_assign_saturday.short_description = "Assign Saturday"


def aa_assign_sunday(modeladmin, request, queryset):
    for x in queryset:
        x.assigned_day = "sunday"
        x.save()


aa_assign_sunday.short_description = "Assign Sunday"


class ArtistAlleyAdmin(ImportExportModelAdmin):
    actions = [aa_generate_manual_mailing, aa_send_space_reservation, aa_send_waitlist, aa_assign_friday, aa_assign_saturday, aa_assign_sunday]
    list_display = ['table_name', 'email', 'first_name', 'last_name', 'availability', 'assigned_day', 'types_of_wares', 'waitlisted']
    list_filter = ('availability', 'assigned_day', 'types_of_wares', 'waitlisted', 'event')


class TableAssignmentAdmin(ImportExportModelAdmin):
    list_display = ['get_business_name', 'get_table_designation', 'get_dealer_slug']


class HotTableAdmin(ImportExportModelAdmin):
    list_display = ['dealer', 'selected_day', 'date_created']
    list_filter = ['event', 'dealer__area', 'selected_day']


class TableDefinitionAdmin(ImportExportModelAdmin):
    list_filter = ['map_key', 'map_key__event']
    list_display = ['designation', 'map_key']


class InvoiceAdmin(ImportExportModelAdmin):
    list_display = ['user', 'paid', 'date_paid']
    list_filter = ['paid']


admin.site.register(TableSize, TableSizeAdmin)
admin.site.register(Dealer, DealerAdmin)
admin.site.register(ArtistAlley, ArtistAlleyAdmin)
admin.site.register(Invoice, InvoiceAdmin)
admin.site.register(TableDefinition, TableDefinitionAdmin)
admin.site.register(TableAssignment, TableAssignmentAdmin)
admin.site.register(HotTable, HotTableAdmin)
