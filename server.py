<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Free Local TTS</title>
    <style>
      :root {
        --bg: #0b1120;
        --panel: #111827;
        --panel2: #1f2937;
        --muted: #94a3b8;
        --text: #e5eefb;
        --line: rgba(148, 163, 184, 0.28);
        --primary: #8b5cf6;
        --primary-2: #ec4899;
        --success: #31c48d;
        --warning: #fbbf24;
        --danger: #f87171;
      }

      * { box-sizing: border-box; }
      body {
        margin: 0;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
        background: linear-gradient(135deg, #020817, #111827 35%, #1e293b 100%);
        color: var(--text);
        min-height: 100vh;
        padding: 24px;
      }

      .app {
        max-width: 1100px;
        margin: 0 auto;
        background: rgba(17, 24, 39, 0.92);
        border: 1px solid var(--line);
        border-radius: 24px;
        padding: 24px;
        box-shadow: 0 20px 60px rgba(0,0,0,0.35);
      }

      h1 {
        margin: 0 0 8px;
        font-size: clamp(28px, 4vw, 44px);
        background: linear-gradient(135deg, #a78bfa, #f472b6);
        -webkit-background-clip: text;
        background-clip: text;
        color: transparent;
      }

      .subtitle {
        color: var(--muted);
        margin-bottom: 24px;
      }

      .layout {
        display: grid;
        grid-template-columns: 1.2fr 0.8fr;
        gap: 24px;
      }

      .panel {
        background: rgba(31, 41, 55, 0.8);
        border: 1px solid var(--line);
        border-radius: 18px;
        padding: 18px;
      }

      .form-row {
        margin-bottom: 16px;
      }

      label {
        display: block;
        font-size: 12px;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        color: #dbeafe;
        margin-bottom: 8px;
        font-weight: 700;
      }

      textarea,
      select,
      input[type="text"] {
        width: 100%;
        padding: 14px 16px;
        background: rgba(15, 23, 42, 0.95);
        border: 1px solid var(--line);
        border-radius: 12px;
        color: var(--text);
        font-size: 15px;
      }

      textarea {
        min-height: 180px;
        resize: vertical;
      }

      .toolbar {
        display: flex;
        flex-wrap: wrap;
        gap: 12px;
      }

      button {
        border: none;
        border-radius: 12px;
        padding: 12px 18px;
        font-size: 14px;
        font-weight: 700;
        cursor: pointer;
        transition: transform 0.2s ease;
      }

      button:hover { transform: translateY(-1px); }

      .primary {
        background: linear-gradient(135deg, var(--primary), var(--primary-2));
        color: white;
      }

      .secondary {
        background: rgba(148, 163, 184, 0.12);
        color: var(--text);
        border: 1px solid var(--line);
      }

      .danger {
        background: rgba(248, 113, 113, 0.12);
        color: #fecaca;
        border: 1px solid rgba(248, 113, 113, 0.26);
      }

      .meta-row {
        display: flex;
        gap: 12px;
        flex-wrap: wrap;
        justify-content: space-between;
        margin-top: 18px;
        color: var(--muted);
        font-size: 13px;
      }

      .pill {
        display: inline-block;
        padding: 8px 10px;
        border-radius: 999px;
        border: 1px solid var(--line);
        background: rgba(148,163,184,0.08);
      }

      .status {
        margin-top: 16px;
        min-height: 48px;
        border-radius: 12px;
        padding: 12px 14px;
        display: none;
        font-size: 14px;
      }

      .status.show { display: block; }
      .status.info { background: rgba(59,130,246,0.12); color: #bfdbfe; border: 1px solid rgba(59,130,246,0.22); }
      .status.success { background: rgba(52,211,153,0.12); color: #bbf7d0; border: 1px solid rgba(52,211,153,0.24); }
      .status.error { background: rgba(248,113,113,0.12); color: #fecaca; border: 1px solid rgba(248,113,113,0.25); }

      .voice-box,
      .history-box {
        margin-top: 14px;
      }

      .audio-card {
        margin-top: 12px;
        border: 1px solid var(--line);
        border-radius: 12px;
        background: rgba(15, 23, 42, 0.8);
        padding: 14px;
      }

      audio {
        width: 100%;
        margin: 10px 0;
      }

      .progress-wrap {
        display: flex;
        align-items: center;
        gap: 10px;
        margin-top: 8px;
      }

      .progress-bar {
        flex: 1;
        height: 8px;
        background: rgba(148,163,184,0.2);
        border-radius: 999px;
        overflow: hidden;
      }

      .progress-fill {
        width: 0%;
        height: 100%;
        background: linear-gradient(90deg, var(--primary), var(--primary-2));
      }

      ul {
        list-style: none;
        padding: 0;
        margin: 0;
      }

      .history-item {
        border: 1px solid var(--line);
        border-radius: 12px;
        background: rgba(15,23,42,0.7);
        padding: 12px;
        margin-top: 10px;
      }

      .history-preview {
        color: var(--muted);
        font-size: 13px;
        line-height: 1.5;
        margin-top: 6px;
      }

      .small-link {
        color: #c4b5fd;
        text-decoration: none;
        font-weight: 600;
      }

      @media (max-width: 800px) {
        .layout { grid-template-columns: 1fr; }
      }
    </style>
  </head>
  <body>
    <div class="app">
      <h1>Free Local TTS</h1>
      <div class="subtitle">Generate spoken audio using your selected voice sample, locally and without paid APIs.</div>

      <div class="layout">
        <div class="panel">
          <div class="form-row">
            <label for="textInput">Text to speak</label>
            <textarea id="textInput" placeholder="Type or paste any text here...">नमस्ते, यह मेरा आवाज़ परीक्षण है।</textarea>
          </div>

          <div class="form-row">
            <label for="languageSelect">Language</label>
            <select id="languageSelect">
              <option value="auto">Auto Detect</option>
              <option value="en">English</option>
              <option value="hi">Hindi</option>
              <option value="gu">Gujarati</option>
            </select>
          </div>

          <div class="toolbar">
            <button id="generateBtn" class="primary">Generate Speech</button>
            <button id="playBtn" class="secondary">Play</button>
            <button id="pauseBtn" class="secondary">Pause</button>
            <button id="clearBtn" class="danger">Clear Text</button>
          </div>

          <div class="meta-row">
            <span class="pill" id="voiceDisplay">Voice: Default reference</span>
            <span class="pill" id="statusPill">Status: Idle</span>
          </div>

          <div id="statusMsg" class="status"></div>

          <div class="audio-card">
            <div style="font-size:12px; text-transform:uppercase; letter-spacing:0.08em; color:#dbeafe; font-weight:700; margin-bottom:8px;">Preview</div>
            <audio id="audioPlayer" controls></audio>
            <div class="progress-wrap">
              <div class="progress-bar"><div id="progressFill" class="progress-fill"></div></div>
              <span id="progressText">0%</span>
            </div>
            <div style="margin-top:12px; display:flex; gap:10px; flex-wrap:wrap;">
              <a id="downloadWav" class="small-link" href="#" download>Download .wav</a>
              <a id="downloadMp3" class="small-link" href="#" download>Download .mp3</a>
            </div>
          </div>
        </div>

        <div class="panel">
          <div class="voice-box">
            <label>Selected voice</label>
            <div class="meta-row" style="margin-top:0; justify-content:flex-start;">
              <span class="pill" id="selectedVoiceName">Standard recording 32_20261008192509</span>
            </div>
            <div style="color: var(--muted); margin-top:10px; font-size:13px; line-height:1.5;">
              The default voice reference is saved locally in the browser with the original repository sample.
              If the chosen local XTTS model supports the selected language, the generated speech will use this reference voice whenever available.
            </div>
          </div>

          <div class="history-box">
            <label>Recent audio history</label>
            <ul id="historyList"></ul>
          </div>
        </div>
      </div>
    </div>

    <script>
      const textInput = document.getElementById('textInput');
      const languageSelect = document.getElementById('languageSelect');
      const generateBtn = document.getElementById('generateBtn');
      const playBtn = document.getElementById('playBtn');
      const pauseBtn = document.getElementById('pauseBtn');
      const clearBtn = document.getElementById('clearBtn');
      const statusMsg = document.getElementById('statusMsg');
      const voiceDisplay = document.getElementById('voiceDisplay');
      const selectedVoiceName = document.getElementById('selectedVoiceName');
      const statusPill = document.getElementById('statusPill');
      const audioPlayer = document.getElementById('audioPlayer');
      const progressFill = document.getElementById('progressFill');
      const progressText = document.getElementById('progressText');
      const downloadWav = document.getElementById('downloadWav');
      const downloadMp3 = document.getElementById('downloadMp3');
      const historyList = document.getElementById('historyList');

      const STORAGE_KEY = 'tts-selected-voice';
      const HISTORY_KEY = 'tts-history';

      function setStatus(message, kind='info') {
        statusMsg.textContent = message;
        statusMsg.className = 'status show ' + kind;
        statusPill.textContent = 'Status: ' + (kind === 'success' ? 'Ready' : kind === 'error' ? 'Error' : 'Generating');
      }

      function getSelectedVoice() {
        const defaultName = 'Standard recording 32_20261008192509';
        try {
          const saved = localStorage.getItem(STORAGE_KEY);
          return saved ? JSON.parse(saved) : { voiceId: 'default-reference', name: defaultName, file: 'Standard recording 32_20261008192509.mp3' };
        } catch (err) {
          return { voiceId: 'default-reference', name: defaultName, file: 'Standard recording 32_20261008192509.mp3' };
        }
      }

      function saveSelectedVoice(voice) {
        localStorage.setItem(STORAGE_KEY, JSON.stringify(voice));
      }

      function renderVoiceMeta() {
        const voice = getSelectedVoice();
        voiceDisplay.textContent = 'Voice: ' + (voice.name || 'Default reference');
        selectedVoiceName.textContent = voice.name || 'Standard recording 32_20261008192509';
      }

      function loadHistory() {
        try {
          const rows = JSON.parse(localStorage.getItem(HISTORY_KEY) || '[]');
          historyList.innerHTML = '';
          if (!rows.length) {
            historyList.innerHTML = '<li class="history-item"><div style="color:var(--muted);">No generated audio yet.</div></li>';
            return;
          }

          rows.slice(0, 6).forEach((item) => {
            const el = document.createElement('li');
            el.className = 'history-item';
            el.innerHTML = `
              <div style="font-weight:700;">${item.language.toUpperCase()}</div>
              <div class="history-preview">${(item.text || '').slice(0, 120)}</div>
              <div style="margin-top:8px;"><a class="small-link" href="${item.url}" target="_blank" rel="noopener">Open audio</a></div>
            `;
            historyList.appendChild(el);
          });
        } catch (err) {
          historyList.innerHTML = '<li class="history-item"><div style="color:var(--muted);">No generated audio yet.</div></li>';
        }
      }

      function persistHistoryItem(item) {
        try {
          const rows = JSON.parse(localStorage.getItem(HISTORY_KEY) || '[]');
          rows.unshift(item);
          localStorage.setItem(HISTORY_KEY, JSON.stringify(rows.slice(0, 8)));
        } catch (err) {
          console.error('Unable to save history:', err);
        }
      }

      async function generateTTS() {
        const text = textInput.value.trim();
        if (!text) {
          setStatus('Please enter text before generating speech.', 'error');
          return;
        }

        const voice = getSelectedVoice();
        const payload = {
          text,
          language: languageSelect.value,
          voice_id: voice.voiceId || 'default-reference',
          voice_name: voice.name || 'Standard recording 32_20261008192509',
          voice_file: voice.file || 'Standard recording 32_20261008192509.mp3',
          use_reference_voice: true,
          speed: 1.0,
        };

        setStatus('Generating speech with your selected voice reference... Please wait.', 'info');
        generateBtn.disabled = true;
        playBtn.disabled = true;

        try {
          const response = await fetch('/api/tts/generate', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload),
          });

          const data = await response.json();
          if (!response.ok) {
            throw new Error(data.detail || 'Generation failed.');
          }

          const generatedPath = data.audio_path || '';
          const audioUrl = '/api/tts/download/' + encodeURIComponent((generatedPath.split('/').slice(-1)[0] || 'output.wav'));

          audioPlayer.src = audioUrl;
          audioPlayer.load();
          downloadWav.href = audioUrl;
          downloadWav.download = data.download_name || 'generated.wav';
          downloadWav.setAttribute('aria-label', 'Download audio as WAV');

          const mp3Url = '/api/tts/download/' + encodeURIComponent((data.download_name || 'generated.wav').replace(/\.wav$/i, '.mp3'));
          downloadMp3.href = mp3Url;
          downloadMp3.download = (data.download_name || 'generated.wav').replace(/\.wav$/i, '.mp3');

          setStatus(data.message || 'Speech generated successfully.', 'success');
          statusPill.textContent = 'Status: Ready';

          persistHistoryItem({
            text,
            language: languageSelect.value,
            url: audioUrl,
            time: new Date().toISOString(),
          });
          loadHistory();
        } catch (err) {
          console.error(err);
          setStatus(err.message || 'Unable to generate speech with the selected voice. Make sure the local TTS model is configured correctly.', 'error');
        } finally {
          generateBtn.disabled = false;
          playBtn.disabled = false;
        }
      }

      function bindAudioProgress() {
        audioPlayer.addEventListener('timeupdate', () => {
          if (!audioPlayer.duration) return;
          const progress = (audioPlayer.currentTime / audioPlayer.duration) * 100;
          progressFill.style.width = progress + '%';
          progressText.textContent = Math.round(progress) + '%';
        });

        audioPlayer.addEventListener('ended', () => {
          progressFill.style.width = '100%';
          progressText.textContent = '100%';
        });
      }

      generateBtn.addEventListener('click', generateTTS);
      playBtn.addEventListener('click', () => audioPlayer.play());
      pauseBtn.addEventListener('click', () => audioPlayer.pause());
      clearBtn.addEventListener('click', () => {
        textInput.value = '';
        setStatus('Text cleared.', 'info');
      });

      renderVoiceMeta();
      bindAudioProgress();
      loadHistory();
    </script>
  </body>
</html>
