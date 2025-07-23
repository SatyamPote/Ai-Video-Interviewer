document.addEventListener('DOMContentLoaded', () => {
    // --- Element References ---
    const userVideo = document.getElementById('userVideo');
    const startButton = document.getElementById('startButton');
    const resumeFile = document.getElementById('resumeFile');
    const jobDescription = document.getElementById('jobDescription');
    const chatLog = document.getElementById('chatLog');
    const interviewerAudio = document.getElementById('interviewerAudio');
    const setupDiv = document.getElementById('setup');
    const responseControlsDiv = document.getElementById('responseControls');
    const recordButton = document.getElementById('recordButton');
    const statusDiv = document.getElementById('status');

    // --- State Variables ---
    let conversationHistory = "";
    let mediaRecorder;
    let audioChunks = [];
    let isRecording = false;

    // --- UI & Media Functions ---
    function addMessageToLog(text, sender) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${sender}-message`;
        messageDiv.innerHTML = text.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
        chatLog.appendChild(messageDiv);
        chatLog.scrollTop = chatLog.scrollHeight;
    }

    function playAiAudio(audioUrl) {
        interviewerAudio.src = audioUrl;
        interviewerAudio.play().catch(e => console.warn("Autoplay blocked. User interaction needed."));
    }
    
    async function setupMedia() {
        try {
            const stream = await navigator.mediaDevices.getUserMedia({ video: true, audio: true });
            userVideo.srcObject = stream;
            mediaRecorder = new MediaRecorder(stream);
            mediaRecorder.ondataavailable = event => event.data.size > 0 && audioChunks.push(event.data);
            mediaRecorder.onstop = handleRecordingStop;
            startButton.disabled = false;
            statusDiv.textContent = "Ready. Please fill out the setup.";
        } catch (err) {
            statusDiv.innerHTML = "<strong>Error:</strong> Webcam/Mic access denied. Please grant permissions and refresh.";
        }
    }

    async function handleRecordingStop() {
        if (audioChunks.length === 0) return;

        statusDiv.textContent = 'Processing your answer...';
        recordButton.disabled = true;

        const audioBlob = new Blob(audioChunks, { type: 'audio/webm' });
        audioChunks = [];

        const formData = new FormData();
        formData.append('audio', audioBlob, 'response.webm');
        formData.append('conversation_history', conversationHistory);

        try {
            const response = await fetch('http://127.0.0.1:5001/process-response', {
                method: 'POST',
                body: formData,
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.error || 'Unknown server error');
            }

            const data = await response.json();
            
            addMessageToLog(`<strong>You:</strong> ${data.transcription}`, 'user');
            addMessageToLog(data.ai_response, 'ai');
            
            conversationHistory = data.conversation;

            playAiAudio(data.audio_url);
            statusDiv.textContent = 'Ready for your next answer.';
        } catch (error) {
            console.error('Error processing response:', error);
            statusDiv.textContent = `Error: ${error.message}. Please try again.`;
        } finally {
            recordButton.disabled = false;
        }
    }

    // --- Event Listeners ---
    startButton.addEventListener('click', async () => {
        if (!resumeFile.files.length || !jobDescription.value) {
            alert('Please upload a resume and provide a job description.');
            return;
        }

        startButton.textContent = 'Starting...';
        startButton.disabled = true;
        statusDiv.textContent = 'Contacting AI... This may take a moment.';

        const formData = new FormData();
        formData.append('resume', resumeFile.files[0]);
        formData.append('job_desc', jobDescription.value);

        try {
            const response = await fetch('http://127.0.0.1:5001/start-interview', {
                method: 'POST',
                body: formData,
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.error || 'Unknown server error');
            }

            const data = await response.json();
            conversationHistory = data.conversation;
            
            chatLog.innerHTML = '';
            
            // ================================================================
            // === FINAL FIX FOR MULTIPLE STARTING MESSAGES ===
            // ================================================================
            const initialText = data.conversation;
            
            // This is the robust fix: Split by the newline character.
            // This will correctly handle any number of starting lines.
            const lines = initialText.split('\n').filter(line => line.trim() !== '');

            // Loop through each line and create a separate, clean chat bubble for it.
            lines.forEach(line => {
                addMessageToLog(line, 'ai');
            });
            // ================================================================

            // The server correctly generates audio for just the last line (the actual question),
            // so we can play the audio URL directly without any changes.
            playAiAudio(data.audio_url);
            
            setupDiv.style.display = 'none';
            responseControlsDiv.style.display = 'flex';
            statusDiv.textContent = 'Interview started.';
        } catch (error) {
            console.error('Error starting interview:', error);
            statusDiv.textContent = `Error: ${error.message}. Please refresh and try again.`;
            startButton.textContent = 'Start Interview';
            startButton.disabled = false;
        }
    });

    recordButton.addEventListener('click', () => {
        if (isRecording) {
            mediaRecorder.stop();
            recordButton.textContent = 'Record Answer';
            recordButton.classList.remove('recording');
            isRecording = false;
        } else {
            mediaRecorder.start();
            recordButton.textContent = 'Stop Recording';
            recordButton.classList.add('recording');
            statusDiv.textContent = 'Recording...';
            isRecording = true;
        }
    });

    // --- Initial Call ---
    setupMedia();
});