export default async function handler(req, res) {
  const method = req.method || 'GET';

  if (method === 'GET') {
    return res.status(200).json({
      configured: Boolean(process.env.ELEVENLABS_API_KEY),
      hasVoiceId: Boolean(process.env.ELEVENLABS_VOICE_ID),
      note: 'Set ELEVENLABS_API_KEY and ELEVENLABS_VOICE_ID in Vercel Environment Variables to enable custom voice cloning from your MP3 reference.'
    });
  }

  if (method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  if (!process.env.ELEVENLABS_API_KEY) {
    return res.status(500).json({
      error: 'ELEVENLABS_API_KEY is not configured in Vercel. Add it under Project > Settings > Environment Variables before generating custom voice audio.'
    });
  }

  const chunks = [];
  for await (const chunk of req) {
    chunks.push(Buffer.isBuffer(chunk) ? chunk : Buffer.from(chunk));
  }

  let body = {};
  if (chunks.length > 0) {
    const raw = Buffer.concat(chunks).toString('utf8');
    if (raw.trim()) {
      try {
        body = JSON.parse(raw);
      } catch {
        return res.status(400).json({ error: 'Request body must be valid JSON.' });
      }
    }
  }

  const action = body.action || 'tts';

  try {
    if (action === 'create-voice') {
      const dataUrl = body.voiceReferenceDataUrl;
      const voiceName = body.voiceName || 'My reference voice';
      if (!dataUrl) {
        return res.status(400).json({ error: 'voiceReferenceDataUrl is required for create-voice.' });
      }

      const base64 = dataUrl.includes(',') ? dataUrl.split(',')[1] : dataUrl;
      const mimeType = body.mimeType || 'audio/mpeg';
      const fileBuffer = Buffer.from(base64, 'base64');
      const form = new FormData();
      form.append('name', voiceName);
      form.append('files', new Blob([fileBuffer], { type: mimeType }), body.fileName || 'reference.mp3');

      const voiceResponse = await fetch('https://api.elevenlabs.io/v1/voices/add', {
        method: 'POST',
        headers: {
          'xi-api-key': process.env.ELEVENLABS_API_KEY
        },
        body: form
      });

      const voiceJson = await voiceResponse.json();
      if (!voiceResponse.ok) {
        return res.status(500).json({
          error: 'ElevenLabs voice creation failed.',
          details: voiceJson
        });
      }

      return res.status(200).json({
        ok: true,
        voice_id: voiceJson.voice_id || voiceJson.voiceId || voiceJson.id,
        voice_name: voiceJson.name || voiceName,
        message: 'Custom voice created. Save the returned voice_id in Vercel environment variables as ELEVENLABS_VOICE_ID.'
      });
    }

    if (action === 'tts') {
      const text = String(body.text || '').trim();
      const voiceId = body.voiceId || process.env.ELEVENLABS_VOICE_ID;
      if (!text) {
        return res.status(400).json({ error: 'Text is required.' });
      }
      if (!voiceId) {
        return res.status(400).json({
          error: 'ELEVENLABS_VOICE_ID is not configured. Add it to Vercel Environment Variables after creating the custom voice in ElevenLabs.'
        });
      }

      const response = await fetch(`https://api.elevenlabs.io/v1/text-to-speech/${voiceId}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'xi-api-key': process.env.ELEVENLABS_API_KEY
        },
        body: JSON.stringify({
          text,
          model_id: body.modelId || 'eleven_multilingual_v2',
          voice_settings: {
            stability: Number(body.stability ?? 0.5),
            similarity_boost: Number(body.similarityBoost ?? 0.75)
          }
        })
      });

      const arrayBuffer = await response.arrayBuffer();
      if (!response.ok) {
        const errorText = Buffer.from(arrayBuffer).toString('utf8');
        return res.status(500).json({
          error: 'ElevenLabs speech generation failed.',
          details: errorText
        });
      }

      res.setHeader('Content-Type', 'audio/mpeg');
      res.setHeader('Content-Disposition', 'attachment; filename="custom-voice-output.mp3"');
      return res.status(200).send(Buffer.from(arrayBuffer));
    }

    return res.status(400).json({ error: 'Unknown action. Use create-voice or tts.' });
  } catch (error) {
    return res.status(500).json({
      error: 'Unexpected server error.',
      message: error.message || 'Unknown error'
    });
  }
}
