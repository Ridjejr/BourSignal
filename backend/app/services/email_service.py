import smtplib
from email.message import EmailMessage

from flask import current_app


class EmailService:
    """Envoi d'emails via SMTP (Gmail par défaut).

    Si aucun identifiant SMTP n'est configuré, on ne plante pas :
    on logue simplement le contenu du mail (mode dev). Ça permet de
    développer/tester sans compte SMTP.
    """

    @staticmethod
    def envoyer(destinataire, sujet, corps_html):
        cfg = current_app.config
        user = cfg.get("SMTP_USER")
        password = cfg.get("SMTP_PASSWORD")

        # Mode dev : pas de SMTP configuré -> on logue au lieu d'envoyer.
        if not user or not password:
            current_app.logger.warning(
                "[EMAIL MODE DEV] SMTP non configuré — mail NON envoyé.\n"
                "  À : %s\n  Sujet : %s\n%s",
                destinataire, sujet, corps_html,
            )
            return False

        message = EmailMessage()
        message["Subject"] = sujet
        message["From"] = cfg.get("EMAIL_FROM") or user
        message["To"] = destinataire
        message.set_content(
            "Votre client mail n'affiche pas le HTML. "
            "Ouvre ce message dans un client compatible."
        )
        message.add_alternative(corps_html, subtype="html")

        # Connexion SMTP sécurisée (STARTTLS), puis authentification.
        with smtplib.SMTP(cfg.get("SMTP_HOST"), cfg.get("SMTP_PORT"), timeout=10) as serveur:
            serveur.starttls()
            serveur.login(user, password)
            serveur.send_message(message)

        current_app.logger.info("Email envoyé à %s — %s", destinataire, sujet)
        return True
