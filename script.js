// Pulse Trading Presentation SPA with Ollama AI Integration and Audio Narration
class PulseTradingPresentation {
    constructor() {
        this.currentSlide = 1;
        this.totalSlides = 15;
        this.isPlaying = false;
        this.isPaused = false;
        this.currentUtterance = null;
        this.speechSynthesis = window.speechSynthesis;
        this.voices = [];
        this.selectedVoice = null;
        this.playbackSpeed = 1.0;
        this.autoAdvance = true;
        this.isTransitioning = false;
        this.progressInterval = null;
        this.slideStartTime = null;
        this.slideTimings = {
            1: 45,   // Title slide - 45 seconds
            2: 60,   // Problem & Solution - 60 seconds
            3: 75,   // Market Analysis - 75 seconds
            4: 50,   // Strategic Objectives - 50 seconds
            5: 55,   // Value Proposition - 55 seconds
            6: 70,   // Customer Journey - 70 seconds
            7: 65,   // Marketing Mix - 65 seconds
            8: 60,   // Decision Journey - 60 seconds
            9: 50,   // Service Excellence - 50 seconds
            10: 70,  // Financial Projections - 70 seconds
            11: 65,  // Performance Tracking - 65 seconds
            12: 55,  // Survey Validation - 55 seconds
            13: 60,  // Team Contributions - 60 seconds
            14: 70,  // Implementation Timeline - 70 seconds
            15: 80   // Next Steps - 80 seconds
        };
        this.speakerNotes = {
            1: "Welcome to our Pulse Trading Final Marketing Plan. This presentation outlines our data-driven, community-focused strategy to scale our platform and deliver strong ROI for investors.",
            2: "Everyday investors face a critical gap: they're either overwhelmed by institutional-grade complexity or underserved by basic platforms. Pulse Trading solves this by delivering professional-grade analytics in a community-driven, mobile-first experience.",
            3: "Our comprehensive PEST and SWOT analysis reveals a perfect storm of opportunity. Regulatory support for fintech innovation, explosive growth in retail investing, and a digital-native generation demanding mobile-first experiences create an ideal market entry window.",
            4: "Our SMART objectives are designed to demonstrate clear traction to investors while building a sustainable growth foundation. Each target is specific, measurable, and directly tied to our value proposition.",
            5: "Our value proposition directly addresses the three core jobs our customers need to accomplish: making informed trades, learning from others, and accessing professional tools. We eliminate their biggest pain points while delivering the gains they most desire.",
            6: "Our target customer is the digital-native investor who's comfortable with technology but wants more than basic trading tools. They're active on social media, value community input, and make data-driven decisions.",
            7: "Our integrated marketing mix creates a cohesive strategy that addresses each customer touchpoint. The freemium model removes barriers to entry while premium features capture value.",
            8: "Our customer journey strategy addresses each decision stage with targeted tactics. We recognize that modern investors research extensively before committing, so we provide educational content and social proof throughout their journey.",
            9: "Service excellence is critical in financial services. Our people, process, and physical evidence all reinforce our brand promise of professional-grade tools with community support.",
            10: "Our disciplined budget allocation ensures optimal ROI while building sustainable growth. The 2.5x return demonstrates strong unit economics, and our break-even timeline shows realistic path to profitability.",
            11: "Our KPI framework ensures we stay on track while maintaining flexibility to adapt. Monthly reviews allow for quick course corrections, while quarterly assessments enable strategic pivots.",
            12: "Our survey results provide strong validation for our strategy. The high percentages across all key metrics demonstrate clear product-market fit. Most importantly, 70% willingness to pay premium pricing validates our revenue model.",
            13: "Our team brings diverse expertise across all critical areas of marketing strategy. Each member leads their domain while collaborating closely with others. This structure ensures deep expertise in each area while maintaining integrated execution.",
            14: "Our phased approach ensures steady progress while allowing for learning and optimization. Each phase builds on the previous one, with clear milestones that demonstrate traction to investors.",
            15: "We're ready to move from strategy to execution. Our plan is comprehensive, our team is committed, and our market opportunity is validated. We're seeking $500K in funding to execute this strategy and capture the significant market opportunity we've identified."
        };
        
        this.init();
    }

    init() {
        this.setupEventListeners();
        this.updateSlideCounter();
        this.updateSpeakerNotes();
        this.setupKeyboardNavigation();
        this.initializeAI();
        this.initializeAudio();
    }

    setupEventListeners() {
        // Navigation buttons
        document.getElementById('prevBtn').addEventListener('click', () => this.previousSlide());
        document.getElementById('nextBtn').addEventListener('click', () => this.nextSlide());
        document.getElementById('fullscreenBtn').addEventListener('click', () => this.toggleFullscreen());
        
        // Speaker notes toggle
        document.getElementById('toggleNotes').addEventListener('click', () => this.toggleSpeakerNotes());
        
        // AI panel toggle
        document.getElementById('toggleAI').addEventListener('click', () => this.toggleAIPanel());
        
        // AI enhancement buttons
        document.getElementById('enhanceContent').addEventListener('click', () => this.enhanceContent());
        document.getElementById('generateInsights').addEventListener('click', () => this.generateInsights());
        document.getElementById('improveNarrative').addEventListener('click', () => this.improveNarrative());
        
        // Audio controls
        document.getElementById('playPauseBtn').addEventListener('click', () => this.togglePlayPause());
        document.getElementById('stopBtn').addEventListener('click', () => this.stopNarration());
        document.getElementById('voiceSelect').addEventListener('change', (e) => this.selectVoice(e.target.value));
        document.getElementById('speedSlider').addEventListener('input', (e) => this.setPlaybackSpeed(e.target.value));
        
        // Progress bar click
        document.querySelector('.progress-bar').addEventListener('click', (e) => this.seekToPosition(e));
    }

    setupKeyboardNavigation() {
        document.addEventListener('keydown', (e) => {
            switch(e.key) {
                case 'ArrowLeft':
                case 'ArrowUp':
                    e.preventDefault();
                    this.previousSlide();
                    break;
                case 'ArrowRight':
                case 'ArrowDown':
                    e.preventDefault();
                    this.nextSlide();
                    break;
                case ' ':
                    e.preventDefault();
                    if (this.isPlaying || this.isPaused) {
                        this.togglePlayPause();
                    } else {
                        this.nextSlide();
                    }
                    break;
                case 'f':
                case 'F':
                    e.preventDefault();
                    this.toggleFullscreen();
                    break;
                case 'n':
                case 'N':
                    e.preventDefault();
                    this.toggleSpeakerNotes();
                    break;
                case 'a':
                case 'A':
                    e.preventDefault();
                    this.toggleAIPanel();
                    break;
                case 'Escape':
                    this.exitFullscreen();
                    break;
            }
        });
    }

    nextSlide() {
        if (this.currentSlide < this.totalSlides && !this.isTransitioning) {
            this.isTransitioning = true;
            
            // Add transition classes for smooth animation
            const currentSlideElement = document.querySelector(`[data-slide="${this.currentSlide}"]`);
            const nextSlideElement = document.querySelector(`[data-slide="${this.currentSlide + 1}"]`);
            
            if (currentSlideElement && nextSlideElement) {
                currentSlideElement.classList.add('prev');
                nextSlideElement.classList.add('next');
                
                setTimeout(() => {
                    currentSlideElement.classList.remove('active', 'prev');
                    nextSlideElement.classList.remove('next');
                    nextSlideElement.classList.add('active');
                    
                    this.currentSlide++;
                    this.updateSlide();
                    this.isTransitioning = false;
                }, 300);
            } else {
                this.currentSlide++;
                this.updateSlide();
                this.isTransitioning = false;
            }
        }
    }

    previousSlide() {
        if (this.currentSlide > 1 && !this.isTransitioning) {
            this.isTransitioning = true;
            
            // Add transition classes for smooth animation
            const currentSlideElement = document.querySelector(`[data-slide="${this.currentSlide}"]`);
            const prevSlideElement = document.querySelector(`[data-slide="${this.currentSlide - 1}"]`);
            
            if (currentSlideElement && prevSlideElement) {
                currentSlideElement.classList.add('next');
                prevSlideElement.classList.add('prev');
                
                setTimeout(() => {
                    currentSlideElement.classList.remove('active', 'next');
                    prevSlideElement.classList.remove('prev');
                    prevSlideElement.classList.add('active');
                    
                    this.currentSlide--;
                    this.updateSlide();
                    this.isTransitioning = false;
                }, 300);
            } else {
                this.currentSlide--;
                this.updateSlide();
                this.isTransitioning = false;
            }
        }
    }

    updateSlide() {
        // Remove active class from all slides
        document.querySelectorAll('.slide').forEach(slide => {
            slide.classList.remove('active');
        });

        // Add active class to current slide
        const currentSlideElement = document.querySelector(`[data-slide="${this.currentSlide}"]`);
        if (currentSlideElement) {
            currentSlideElement.classList.add('active');
        }

        this.updateSlideCounter();
        this.updateSpeakerNotes();
        this.updateNavigationButtons();
    }

    updateSlideCounter() {
        document.getElementById('slideCounter').textContent = `${this.currentSlide} / ${this.totalSlides}`;
    }

    updateSpeakerNotes() {
        const notesText = document.getElementById('notesText');
        if (notesText && this.speakerNotes[this.currentSlide]) {
            notesText.textContent = this.speakerNotes[this.currentSlide];
        }
    }

    updateNavigationButtons() {
        const prevBtn = document.getElementById('prevBtn');
        const nextBtn = document.getElementById('nextBtn');
        
        prevBtn.disabled = this.currentSlide === 1;
        nextBtn.disabled = this.currentSlide === this.totalSlides;
    }

    toggleFullscreen() {
        if (!document.fullscreenElement) {
            document.documentElement.requestFullscreen().catch(err => {
                console.log('Error attempting to enable fullscreen:', err);
            });
        } else {
            document.exitFullscreen();
        }
    }

    exitFullscreen() {
        if (document.fullscreenElement) {
            document.exitFullscreen();
        }
    }

    toggleSpeakerNotes() {
        const notesPanel = document.getElementById('speakerNotes');
        const toggleBtn = document.getElementById('toggleNotes');
        const icon = toggleBtn.querySelector('i');
        
        notesPanel.classList.toggle('visible');
        
        if (notesPanel.classList.contains('visible')) {
            icon.className = 'fas fa-eye-slash';
        } else {
            icon.className = 'fas fa-eye';
        }
    }

    toggleAIPanel() {
        const aiPanel = document.getElementById('aiPanel');
        const toggleBtn = document.getElementById('toggleAI');
        const icon = toggleBtn.querySelector('i');
        
        aiPanel.classList.toggle('visible');
        
        if (aiPanel.classList.contains('visible')) {
            icon.className = 'fas fa-chevron-down';
        } else {
            icon.className = 'fas fa-chevron-up';
        }
    }

    initializeAI() {
        // Check if Ollama is available
        this.checkOllamaConnection();
    }

    async checkOllamaConnection() {
        try {
            const response = await fetch('http://localhost:11434/api/tags');
            if (response.ok) {
                this.ollamaAvailable = true;
                console.log('Ollama connection established');
            } else {
                this.ollamaAvailable = false;
                console.log('Ollama not available');
            }
        } catch (error) {
            this.ollamaAvailable = false;
            console.log('Ollama not available:', error);
        }
    }

    async enhanceContent() {
        const output = document.getElementById('aiOutput');
        output.innerHTML = '<p><i class="fas fa-spinner fa-spin"></i> Enhancing content with AI...</p>';

        if (!this.ollamaAvailable) {
            output.innerHTML = '<p>Ollama is not available. Please ensure Ollama is running locally.</p>';
            return;
        }

        try {
            const currentSlideContent = this.getCurrentSlideContent();
            const prompt = `Enhance the following presentation slide content for a professional business presentation about Pulse Trading, a fintech platform for retail investors. Make it more compelling and data-driven:

${currentSlideContent}

Provide specific improvements and additional insights that would strengthen this slide for a VC presentation.`;

            const response = await fetch('http://localhost:11434/api/generate', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    model: 'llama3.2',
                    prompt: prompt,
                    stream: false
                })
            });

            if (response.ok) {
                const data = await response.json();
                output.innerHTML = `<div class="ai-enhancement">
                    <h4>AI Enhancement Suggestions:</h4>
                    <p>${data.response}</p>
                </div>`;
            } else {
                throw new Error('Failed to get AI response');
            }
        } catch (error) {
            output.innerHTML = `<p>Error enhancing content: ${error.message}</p>`;
        }
    }

    async generateInsights() {
        const output = document.getElementById('aiOutput');
        output.innerHTML = '<p><i class="fas fa-spinner fa-spin"></i> Generating insights...</p>';

        if (!this.ollamaAvailable) {
            output.innerHTML = '<p>Ollama is not available. Please ensure Ollama is running locally.</p>';
            return;
        }

        try {
            const prompt = `Based on the Pulse Trading marketing plan presentation, generate 3-5 key strategic insights that would be valuable for investors and stakeholders. Focus on market opportunities, competitive advantages, and growth potential. Be specific and data-driven.`;

            const response = await fetch('http://localhost:11434/api/generate', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    model: 'llama3.2',
                    prompt: prompt,
                    stream: false
                })
            });

            if (response.ok) {
                const data = await response.json();
                output.innerHTML = `<div class="ai-insights">
                    <h4>Strategic Insights:</h4>
                    <p>${data.response}</p>
                </div>`;
            } else {
                throw new Error('Failed to get AI response');
            }
        } catch (error) {
            output.innerHTML = `<p>Error generating insights: ${error.message}</p>`;
        }
    }

    async improveNarrative() {
        const output = document.getElementById('aiOutput');
        output.innerHTML = '<p><i class="fas fa-spinner fa-spin"></i> Improving narrative...</p>';

        if (!this.ollamaAvailable) {
            output.innerHTML = '<p>Ollama is not available. Please ensure Ollama is running locally.</p>';
            return;
        }

        try {
            const currentSlideContent = this.getCurrentSlideContent();
            const prompt = `Improve the narrative flow and storytelling for this presentation slide about Pulse Trading. Make it more engaging and persuasive for a VC audience. Focus on creating a compelling story that connects with investors:

${currentSlideContent}

Provide an improved narrative that maintains the key information while making it more compelling and memorable.`;

            const response = await fetch('http://localhost:11434/api/generate', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    model: 'llama3.2',
                    prompt: prompt,
                    stream: false
                })
            });

            if (response.ok) {
                const data = await response.json();
                output.innerHTML = `<div class="ai-narrative">
                    <h4>Improved Narrative:</h4>
                    <p>${data.response}</p>
                </div>`;
            } else {
                throw new Error('Failed to get AI response');
            }
        } catch (error) {
            output.innerHTML = `<p>Error improving narrative: ${error.message}</p>`;
        }
    }

    getCurrentSlideContent() {
        const currentSlideElement = document.querySelector(`[data-slide="${this.currentSlide}"]`);
        if (currentSlideElement) {
            return currentSlideElement.textContent.trim();
        }
        return '';
    }

    // Enhanced progress tracking for seamless UX
    startProgressTracking() {
        this.clearProgressInterval();
        this.progressInterval = setInterval(() => {
            this.updateProgress();
        }, 100); // Update every 100ms for smooth progress
    }

    clearProgressInterval() {
        if (this.progressInterval) {
            clearInterval(this.progressInterval);
            this.progressInterval = null;
        }
    }

    updateProgress() {
        if (!this.isPlaying || !this.slideStartTime) return;

        const currentTime = Date.now();
        const elapsed = (currentTime - this.slideStartTime) / 1000; // Convert to seconds
        const totalTime = this.slideTimings[this.currentSlide];
        
        const progressPercent = Math.min((elapsed / totalTime) * 100, 100);
        
        // Update progress bar
        const progressFill = document.getElementById('progressFill');
        if (progressFill) {
            progressFill.style.width = `${progressPercent}%`;
        }
        
        // Update time display
        const timeDisplay = document.getElementById('timeDisplay');
        if (timeDisplay) {
            const currentMinutes = Math.floor(elapsed / 60);
            const currentSeconds = Math.floor(elapsed % 60);
            const totalMinutes = Math.floor(totalTime / 60);
            const totalSeconds = Math.floor(totalTime % 60);
            
            timeDisplay.textContent = `${currentMinutes}:${currentSeconds.toString().padStart(2, '0')} / ${totalMinutes}:${totalSeconds.toString().padStart(2, '0')}`;
        }
        
        // Auto-advance when time is up
        if (elapsed >= totalTime && this.autoAdvance) {
            this.autoAdvanceToNextSlide();
        }
    }

    autoAdvanceToNextSlide() {
        if (this.isTransitioning) return;
        
        this.isTransitioning = true;
        this.clearProgressInterval();
        
        // Smooth transition to next slide
        setTimeout(() => {
            if (this.currentSlide < this.totalSlides) {
                this.nextSlide();
                this.isTransitioning = false;
                
                // Continue narration if playing
                if (this.isPlaying) {
                    setTimeout(() => {
                        this.startNarration();
                    }, 500); // Brief pause between slides for better flow
                }
            } else {
                // End of presentation
                this.stopNarration();
                this.isTransitioning = false;
            }
        }, 300); // Transition delay
    }

    // Audio Narration Methods
    initializeAudio() {
        // Load available voices
        this.loadVoices();
        
        // Handle voice loading (some browsers load voices asynchronously)
        if (this.speechSynthesis.onvoiceschanged !== undefined) {
            this.speechSynthesis.onvoiceschanged = () => this.loadVoices();
        }
        
        // Set up speech synthesis event listeners
        this.speechSynthesis.addEventListener('start', () => this.onSpeechStart());
        this.speechSynthesis.addEventListener('end', () => this.onSpeechEnd());
        this.speechSynthesis.addEventListener('error', () => this.onSpeechError());
        
        // Initialize UI
        this.updateAudioUI();
    }

    loadVoices() {
        this.voices = this.speechSynthesis.getVoices();
        const voiceSelect = document.getElementById('voiceSelect');
        
        // Clear existing options except the first one
        voiceSelect.innerHTML = '<option value="auto">Auto Voice</option>';
        
        // Add available voices
        this.voices.forEach((voice, index) => {
            const option = document.createElement('option');
            option.value = index;
            option.textContent = `${voice.name} (${voice.lang})`;
            voiceSelect.appendChild(option);
        });
        
        // Select a professional voice by default
        this.selectBestVoice();
    }

    selectBestVoice() {
        // Prefer English voices with professional-sounding names
        const preferredVoices = [
            'Microsoft David Desktop',
            'Microsoft Zira Desktop',
            'Google US English',
            'Alex',
            'Samantha',
            'Victoria'
        ];
        
        for (const preferred of preferredVoices) {
            const voiceIndex = this.voices.findIndex(voice => 
                voice.name.includes(preferred) && voice.lang.startsWith('en')
            );
            if (voiceIndex !== -1) {
                this.selectVoice(voiceIndex);
                return;
            }
        }
        
        // Fallback to first English voice
        const englishVoice = this.voices.find(voice => voice.lang.startsWith('en'));
        if (englishVoice) {
            const index = this.voices.indexOf(englishVoice);
            this.selectVoice(index);
        }
    }

    selectVoice(voiceIndex) {
        if (voiceIndex === 'auto') {
            this.selectedVoice = null;
        } else {
            this.selectedVoice = this.voices[parseInt(voiceIndex)];
        }
        document.getElementById('voiceSelect').value = voiceIndex;
    }

    setPlaybackSpeed(speed) {
        this.playbackSpeed = parseFloat(speed);
        document.getElementById('speedValue').textContent = `${speed}x`;
        
        // Update current utterance if playing
        if (this.currentUtterance) {
            this.currentUtterance.rate = this.playbackSpeed;
        }
    }

    togglePlayPause() {
        if (this.isPlaying) {
            this.pauseNarration();
        } else if (this.isPaused) {
            this.resumeNarration();
        } else {
            this.startNarration();
        }
    }

    startNarration() {
        if (!this.speakerNotes[this.currentSlide]) {
            console.log('No narration available for this slide');
            return;
        }

        if (this.isTransitioning) return;

        this.isPlaying = true;
        this.isPaused = false;
        this.slideStartTime = Date.now();
        this.updateAudioUI();

        // Start progress tracking
        this.startProgressTracking();

        const utterance = new SpeechSynthesisUtterance(this.speakerNotes[this.currentSlide]);
        
        // Configure speech settings
        utterance.rate = this.playbackSpeed;
        utterance.pitch = 1.0;
        utterance.volume = 0.8;
        
        if (this.selectedVoice) {
            utterance.voice = this.selectedVoice;
        }

        // Set up event listeners for this utterance
        utterance.onstart = () => this.onUtteranceStart();
        utterance.onend = () => this.onUtteranceEnd();
        utterance.onerror = () => this.onUtteranceError();

        this.currentUtterance = utterance;
        this.speechSynthesis.speak(utterance);
    }

    pauseNarration() {
        if (this.isPlaying) {
            this.speechSynthesis.pause();
            this.isPlaying = false;
            this.isPaused = true;
            this.updateAudioUI();
        }
    }

    resumeNarration() {
        if (this.isPaused) {
            this.speechSynthesis.resume();
            this.isPlaying = true;
            this.isPaused = false;
            this.updateAudioUI();
        }
    }

    stopNarration() {
        this.speechSynthesis.cancel();
        this.isPlaying = false;
        this.isPaused = false;
        this.currentUtterance = null;
        this.clearProgressInterval();
        this.updateAudioUI();
        
        // Reset progress bar
        const progressFill = document.getElementById('progressFill');
        if (progressFill) {
            progressFill.style.width = '0%';
        }
        
        // Reset time display
        const timeDisplay = document.getElementById('timeDisplay');
        if (timeDisplay) {
            const totalTime = this.slideTimings[this.currentSlide];
            const totalMinutes = Math.floor(totalTime / 60);
            const totalSeconds = Math.floor(totalTime % 60);
            timeDisplay.textContent = `0:00 / ${totalMinutes}:${totalSeconds.toString().padStart(2, '0')}`;
        }
    }

    onSpeechStart() {
        console.log('Speech started');
    }

    onSpeechEnd() {
        console.log('Speech ended');
        if (this.autoAdvance && this.currentSlide < this.totalSlides) {
            setTimeout(() => {
                this.nextSlide();
                if (this.isPlaying) {
                    this.startNarration();
                }
            }, 1000); // 1 second pause between slides
        } else {
            this.isPlaying = false;
            this.isPaused = false;
            this.updateAudioUI();
        }
    }

    onSpeechError(event) {
        console.error('Speech error:', event.error);
        this.isPlaying = false;
        this.isPaused = false;
        this.updateAudioUI();
    }

    onUtteranceStart() {
        this.startProgressTimer();
    }

    onUtteranceEnd() {
        this.stopProgressTimer();
    }

    onUtteranceError(event) {
        console.error('Utterance error:', event.error);
        this.stopProgressTimer();
    }

    startProgressTimer() {
        const slideDuration = this.slideTimings[this.currentSlide] || 60;
        this.progressStartTime = Date.now();
        this.progressDuration = slideDuration * 1000;
        
        this.progressInterval = setInterval(() => {
            const elapsed = Date.now() - this.progressStartTime;
            const progress = Math.min(elapsed / this.progressDuration, 1);
            this.updateProgress(progress, slideDuration);
        }, 100);
    }

    stopProgressTimer() {
        if (this.progressInterval) {
            clearInterval(this.progressInterval);
            this.progressInterval = null;
        }
    }

    updateProgress(progress, totalDuration) {
        const progressFill = document.getElementById('progressFill');
        const timeDisplay = document.getElementById('timeDisplay');
        
        progressFill.style.width = `${progress * 100}%`;
        
        const currentTime = Math.floor(progress * totalDuration);
        const minutes = Math.floor(currentTime / 60);
        const seconds = currentTime % 60;
        const totalMinutes = Math.floor(totalDuration / 60);
        const totalSeconds = totalDuration % 60;
        
        timeDisplay.textContent = `${minutes}:${seconds.toString().padStart(2, '0')} / ${totalMinutes}:${totalSeconds.toString().padStart(2, '0')}`;
    }

    seekToPosition(event) {
        if (!this.isPlaying && !this.isPaused) return;
        
        const progressBar = event.currentTarget;
        const rect = progressBar.getBoundingClientRect();
        const clickX = event.clientX - rect.left;
        const progress = clickX / rect.width;
        
        // Calculate new position
        const slideDuration = this.slideTimings[this.currentSlide] || 60;
        const newTime = progress * slideDuration;
        
        // Restart narration from new position
        this.stopNarration();
        setTimeout(() => {
            this.startNarration();
            // Note: Browser TTS doesn't support seeking, so we restart from beginning
            // In a production app, you'd use pre-recorded audio files for seeking
        }, 100);
    }

    updateAudioUI() {
        const playPauseBtn = document.getElementById('playPauseBtn');
        const stopBtn = document.getElementById('stopBtn');
        const icon = playPauseBtn.querySelector('i');
        
        if (this.isPlaying) {
            icon.className = 'fas fa-pause';
            playPauseBtn.title = 'Pause Narration';
            stopBtn.disabled = false;
        } else if (this.isPaused) {
            icon.className = 'fas fa-play';
            playPauseBtn.title = 'Resume Narration';
            stopBtn.disabled = false;
        } else {
            icon.className = 'fas fa-play';
            playPauseBtn.title = 'Play Narration';
            stopBtn.disabled = true;
        }
    }
}

// Initialize the presentation when the DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new PulseTradingPresentation();
});

// Add some additional utility functions
class PresentationUtils {
    static formatNumber(num) {
        return new Intl.NumberFormat().format(num);
    }

    static formatCurrency(amount) {
        return new Intl.NumberFormat('en-US', {
            style: 'currency',
            currency: 'USD',
            minimumFractionDigits: 0,
            maximumFractionDigits: 0
        }).format(amount);
    }

    static formatPercentage(value) {
        return new Intl.NumberFormat('en-US', {
            style: 'percent',
            minimumFractionDigits: 0,
            maximumFractionDigits: 1
        }).format(value / 100);
    }

    static animateCounter(element, start, end, duration) {
        const startTime = performance.now();
        const difference = end - start;

        function updateCounter(currentTime) {
            const elapsed = currentTime - startTime;
            const progress = Math.min(elapsed / duration, 1);
            const current = Math.floor(start + (difference * progress));
            
            element.textContent = current;
            
            if (progress < 1) {
                requestAnimationFrame(updateCounter);
            }
        }

        requestAnimationFrame(updateCounter);
    }
}

// Add smooth scrolling and animations
document.addEventListener('DOMContentLoaded', () => {
    // Add intersection observer for animations
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
            }
        });
    }, observerOptions);

    // Observe all slide content for animations
    document.querySelectorAll('.slide-content > *').forEach(el => {
        el.style.opacity = '0';
        el.style.transform = 'translateY(20px)';
        el.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
        observer.observe(el);
    });
});

// Add export functionality
class PresentationExporter {
    static exportToPDF() {
        // This would integrate with a PDF generation library
        console.log('Export to PDF functionality would be implemented here');
    }

    static exportToPowerPoint() {
        // This would integrate with a PowerPoint generation library
        console.log('Export to PowerPoint functionality would be implemented here');
    }

    static exportSpeakerNotes() {
        const notes = document.getElementById('notesText').textContent;
        const blob = new Blob([notes], { type: 'text/plain' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = 'pulse-trading-speaker-notes.txt';
        a.click();
        URL.revokeObjectURL(url);
    }
}

// Add keyboard shortcuts help
document.addEventListener('keydown', (e) => {
    if (e.key === '?' || e.key === '/') {
        e.preventDefault();
        alert(`Keyboard Shortcuts:
• Arrow Keys: Navigate slides
• Space: Play/Pause narration (or next slide if not playing)
• F: Toggle fullscreen
• N: Toggle speaker notes
• A: Toggle AI panel
• Escape: Exit fullscreen
• ?: Show this help

Audio Controls:
• Click Play to start automatic narration
• Adjust speed and voice in audio settings
• Progress bar shows current slide timing
• Auto-advances to next slide when narration ends`);
    }
});
