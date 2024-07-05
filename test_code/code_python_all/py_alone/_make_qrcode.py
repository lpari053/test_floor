import qrcode
from PIL import Image

# Spécifiez le lien de téléchargement
download_link = "https://www.dropbox.com/scl/fi/sqfimc7833za1482s6u8q/app-great2.apk?rlkey=7bdcpi3smv9azwmw9iy4gyla0&st=4xljgj0y&dl=0"

# Créez une instance de QRCode
qr = qrcode.QRCode(
    version=1,  # version: contrôle la taille du QR Code
    error_correction=qrcode.constants.ERROR_CORRECT_L,  # niveau de correction d'erreurs
    box_size=10,  # taille de chaque boîte dans le QR Code
    border=4,  # largeur de la bordure (minimum est 4)
)

# Ajouter les données (le lien de téléchargement) au QRCode
qr.add_data(download_link)
qr.make(fit=True)

# Créez une image de QRCode
img = qr.make_image(fill='black', back_color='white')

# Sauvegardez l'image
img.save("qrcode_download_link.png")

# Afficher l'image
img.show()
