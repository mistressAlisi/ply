from oauth2_provider.oauth2_validators import OAuth2Validator


class CustomOAuth2Validator(OAuth2Validator):
    # Set `oidc_claim_scope = None` to ignore scopes that limit which claims to return,
    # otherwise the OIDC standard scopes are used.

    oidc_claim_scope = OAuth2Validator.oidc_claim_scope
    oidc_claim_scope.update({"name": "name", "email": "email"})

    def get_additional_claims(self, request):
        return {
            "name": request.user.username.lower(),
            "email": request.user.username.lower(),
        }