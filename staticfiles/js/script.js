// Get CSRF token from Django template
const getCSRFToken = () => {
    const csrfInput = document.querySelector('input[name="csrfmiddlewaretoken"]');
    return csrfInput ? csrfInput.value : '';
};

document.addEventListener('DOMContentLoaded', function() {
    // Chat history array and storage functions
    let chatHistory = JSON.parse(localStorage.getItem('chatHistory')) || [];
    
    function saveToHistory(sender, message) {
        chatHistory.push({
            sender: sender,
            message: message,
            timestamp: new Date().toISOString()
        });
        localStorage.setItem('chatHistory', JSON.stringify(chatHistory));
    }
    
    function loadChatHistory() {
        const chatContainer = document.getElementById('id_chat_item_container');
        chatContainer.innerHTML = '';
        chatHistory.forEach(item => {
            const messageClass = item.sender === 'You' ? 'user-message' : 'ai-message';
            chatContainer.innerHTML += `<div class="${messageClass}">${item.sender}: ${item.message}</div>`;
        });
        chatContainer.scrollTop = chatContainer.scrollHeight;
    }

    // Clean response function
    function cleanResponse(text) {
        return text
            .replace(/\*\*/g, '')      
            .replace(/\*/g, '')        
            .replace(/#{1,6}/g, '')   
            .replace(/###/g, '') 
            .replace(/```[\s\S]*?```/g, '\n')  
            .replace(/`/g, '')         
            .replace(/\n{3,}/g, '\n\n') 
            .replace(/\n/g, '<br>')    
            .trim();
    }

    // Load existing chat history when page loads
    loadChatHistory();

    // Handle problem description form submission
    document.getElementById('problem-form').addEventListener('submit', async function(e) {
        e.preventDefault();
        const input = document.getElementById('problem-input').value;
        const chatContainer = document.getElementById('id_chat_item_container');
        
        if (!input) return;
        
        try {
            // Add user message to chat and history
            const userMessage = `You: ${input}`;
            chatContainer.innerHTML += `<div class="user-message">${userMessage}</div>`;
            saveToHistory('You', input);
            
            // Send to API with proper CSRF token
            const response = await fetch('/api/conversation/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCSRFToken()
                },
                body: JSON.stringify({ input: input })
            });
            
            const data = await response.json();
            
            // Add AI response to chat and history
            if (data.response) {
                const cleanMessage = cleanResponse(data.response);
                chatContainer.innerHTML += `<div class="ai-message">AI: ${cleanMessage}</div>`;
                saveToHistory('AI', cleanMessage);
            } else if (data.error) {
                const cleanError = cleanResponse(data.error);
                chatContainer.innerHTML += `<div class="error-message">Error: ${cleanError}</div>`;
                saveToHistory('System', cleanError);
            }
            
        } catch (error) {
            console.error('Error:', error);
            chatContainer.innerHTML += `<div class="error-message">Connection error</div>`;
        }
    });

    // Handle live chat message submission
    document.getElementById('id_message_send_button')?.addEventListener('click', async function() {
        const input = document.getElementById('id_message_send_input').value;
        const chatContainer = document.getElementById('id_chat_item_container');
        
        if (!input) return;
        
        try {
            // Add user message to chat and history
            const userMessage = `You: ${input}`;
            chatContainer.innerHTML += `<div class="user-message">${userMessage}</div>`;
            saveToHistory('You', input);
            
            // Send to API with proper CSRF token
            const response = await fetch('/api/conversation/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCSRFToken()
                },
                body: JSON.stringify({ input: input })
            });
            
            const data = await response.json();
            
            // Add AI response to chat and history
            if (data.response) {
                const cleanMessage = cleanResponse(data.response);
                chatContainer.innerHTML += `<div class="ai-message">AI: ${cleanMessage}</div>`;
                saveToHistory('AI', cleanMessage);
            } else if (data.error) {
                const cleanError = cleanResponse(data.error);
                chatContainer.innerHTML += `<div class="error-message">Error: ${cleanError}</div>`;
                saveToHistory('System', cleanError);
            }
            
            // Clear input
            document.getElementById('id_message_send_input').value = '';
            
        } catch (error) {
            console.error('Error:', error);
            chatContainer.innerHTML += `<div class="error-message">Connection error</div>`;
        }
    });

    // Refresh button functionality - UPDATED TO CLEAR CHAT
    document.getElementById('refresh-chat')?.addEventListener('click', function() {
        // Clear both the display AND the history
        const chatContainer = document.getElementById('id_chat_item_container');
        chatContainer.innerHTML = '';
        chatHistory = [];
        localStorage.removeItem('chatHistory');
    });
});

document.addEventListener('DOMContentLoaded', function() {
    const container = document.getElementById('3d-model-container');
    const width = container.clientWidth;
    const height = container.clientHeight;
    
    // Create scene with custom background color
    const scene = new THREE.Scene();
    scene.background = new THREE.Color(0xA2C4C9); 
    
    const camera = new THREE.PerspectiveCamera(75, width / height, 0.1, 1000);
    const renderer = new THREE.WebGLRenderer({ antialias: true });
    renderer.setSize(width, height);
    container.appendChild(renderer.domElement);
    
    // Add lights 
    const ambientLight = new THREE.AmbientLight(0xffffff, 0.6);
    scene.add(ambientLight);
    
    const directionalLight = new THREE.DirectionalLight(0xffffff, 0.8);
    directionalLight.position.set(1, 1, 1);
    scene.add(directionalLight);
    
    // Add orbit controls
    const controls = new THREE.OrbitControls(camera, renderer.domElement);
    controls.enableDamping = true; 
    controls.dampingFactor = 0.05;
    
    // Load 3D model
    const loader = new THREE.GLTFLoader();
    let model;
    
    loader.load(
        window.MODEL_URL,
        function (gltf) {
            model = gltf.scene;
            scene.add(model);
            
            // Center and scale the model
            const box = new THREE.Box3().setFromObject(model);
            const center = box.getCenter(new THREE.Vector3());
            const size = box.getSize(new THREE.Vector3());
            
            // Calculate scale factor to make model larger
            const scaleFactor = 2.5 / Math.max(size.x, size.y, size.z);
            model.scale.set(scaleFactor, scaleFactor, scaleFactor);
            
            // Reposition model to center
            model.position.x -= center.x * scaleFactor;
            model.position.y -= center.y * scaleFactor;
            model.position.z -= center.z * scaleFactor;
            
            // Set initial camera position
            camera.position.z = 5;
            camera.position.y = 1;
            controls.update();
            
            // Animation loop
            function animate() {
                requestAnimationFrame(animate);
                controls.update(); 
                renderer.render(scene, camera);
            }
            animate();
        },
        undefined,
        function (error) {
            console.error('Error loading 3D model:', error);
            container.innerHTML = '<p>3D model failed to load. Showing default avatar.</p>';
            const img = document.createElement('img');
            img.src = window.FALLBACK_IMAGE;
            img.alt = "Avatar";
            container.appendChild(img);
        }
    );
    

    window.addEventListener('resize', function() {
        camera.aspect = container.clientWidth / container.clientHeight;
        camera.updateProjectionMatrix();
        renderer.setSize(container.clientWidth, container.clientHeight);
    });
});