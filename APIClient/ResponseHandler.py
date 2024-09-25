
class ResponseHandler:
    @staticmethod
    def handle(response):
        """Gère les réponses de l'API en tenant compte des différents codes HTTP et des erreurs spécifiques."""
        status_code = response.status_code
        headers = response.headers
        
        if status_code == 200:
            return response.json(), "success", None
        elif status_code == 429:
            # Too Many Requests: Backoff and retry after the specified time
            retry_after = int(headers.get("Retry-After", 1))
            return None, "retry", retry_after
        elif status_code == 418:
            # IP banned
            retry_after = int(headers.get("Retry-After", 60))
            return None, "ip_banned", retry_after
        elif status_code == 403:
            # Web Application Firewall Limit (WAF) violation
            return None, "error", "WAF Limit violation"
        elif status_code == 409:
            # Partial success in cancelReplace
            return {"partial_success": True, **response.json()}, "partial_success", None
        elif 500 <= status_code < 600:
            # 5XX errors indicate an internal server error
            return None, "retry", 2  # Retry avec backoff exponentiel (géré ailleurs)
        elif 400 <= status_code < 500:
            # 4XX client-side errors
            error_payload = response.json()
            error_code = error_payload.get("code")
            error_message = error_payload.get("msg")
            # Gestion de certains codes d'erreur spécifiques
            if error_code == -1121:
                return None, "error", f"Invalid symbol: {error_message}"
            elif error_code == -2010:
                return None, "error", f"Insufficient balance: {error_message}"
            return None, "error", f"Client error ({status_code}): {error_message} (Code: {error_code})"
        else:
            return None, "error", f"Unexpected response. Status: {status_code}, Response: {response.text}"
