from rest_framework.authentication import TokenAuthentication as BaseToken


class TokenAuthentication(BaseToken):
    keyword = 'Stadino'