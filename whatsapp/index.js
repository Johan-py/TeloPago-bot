const { Client, LocalAuth } = require("whatsapp-web.js");
const qrcode = require("qrcode-terminal");
const axios = require("axios");

const client = new Client({
  authStrategy: new LocalAuth(),
  puppeteer: {
    executablePath: '/usr/bin/google-chrome',
    headless: true,
    args: ['--no-sandbox', '--disable-setuid-sandbox']
  }
});

client.on("qr", (qr) => {
  console.log("📱 Escanea este QR con tu WhatsApp:");
  qrcode.generate(qr, { small: true });
});

client.on("ready", () => {
  console.log("✅ Bot conectado y listo.");
});

client.on('message', async (msg) => {
  console.log(`Mensaje recibido: ${msg.body}`);

  try {
    // Llamamos al backend Flask
    const response = await axios.post('http://localhost:5000/message', {
      message: msg.body
    });

    // Enviamos la respuesta recibida al usuario
    const reply = response.data.reply || "Lo siento, no entendí tu pregunta.";
    msg.reply(reply);

  } catch (error) {
    console.error('Error llamando al backend:', error.message);
    msg.reply('Disculpa, hubo un error al procesar tu solicitud.');
  }
});

client.initialize();
