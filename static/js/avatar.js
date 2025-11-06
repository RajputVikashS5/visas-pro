// static/js/avatar.js
// 3D Animated Avatar with Lip-Sync, Emotions, and Floating Behavior
// Uses Three.js + WebGL + Responsive Design

let scene, camera, renderer, avatar, mouth, eyes;
let isSpeaking = false;
let emotion = 'neutral';
let floatOffset = 0;
let clock = new THREE.Clock();

// Initialize Avatar
function initAvatar() {
    const container = document.body;
    
    // Scene
    scene = new THREE.Scene();
    scene.background = new THREE.Color(0x000000);

    // Camera
    camera = new THREE.PerspectiveCamera(45, 200 / 200, 0.1, 100);
    camera.position.set(0, 0, 5);

    // Renderer
    renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
    renderer.setSize(200, 200);
    renderer.setPixelRatio(window.devicePixelRatio);
    const avatarDiv = document.createElement('div');
    avatarDiv.id = 'visas-avatar';
    avatarDiv.style.position = 'fixed';
    avatarDiv.style.bottom = '20px';
    avatarDiv.style.right = '20px';
    avatarDiv.style.zIndex = '9999';
    avatarDiv.style.cursor = 'pointer';
    avatarDiv.appendChild(renderer.domElement);
    document.body.appendChild(avatarDiv);

    // Light
    const light = new THREE.DirectionalLight(0xffffff, 1);
    light.position.set(5, 5, 5);
    scene.add(light);
    const ambient = new THREE.AmbientLight(0x404040);
    scene.add(ambient);

    // Avatar Body (Sphere Head)
    const headGeometry = new THREE.SphereGeometry(1, 32, 32);
    const headMaterial = new THREE.MeshPhongMaterial({ 
        color: 0x4a90e2,
        shininess: 100
    });
    avatar = new THREE.Mesh(headGeometry, headMaterial);
    scene.add(avatar);

    // Eyes
    const eyeGeometry = new THREE.SphereGeometry(0.15, 16, 16);
    const eyeMaterial = new THREE.MeshPhongMaterial({ color: 0xffffff });
    const leftEye = new THREE.Mesh(eyeGeometry, eyeMaterial);
    leftEye.position.set(-0.4, 0.3, 0.8);
    const rightEye = new THREE.Mesh(eyeGeometry, eyeMaterial);
    rightEye.position.set(0.4, 0.3, 0.8);
    eyes = new THREE.Group();
    eyes.add(leftEye);
    eyes.add(rightEye);
    avatar.add(eyes);

    // Pupils
    const pupilGeometry = new THREE.SphereGeometry(0.07, 16, 16);
    const pupilMaterial = new THREE.MeshPhongMaterial({ color: 0x000000 });
    const leftPupil = new THREE.Mesh(pupilGeometry, pupilMaterial);
    leftPupil.position.set(0, 0, 0.08);
    leftEye.add(leftPupil);
    const rightPupil = new THREE.Mesh(pupilGeometry, pupilMaterial);
    rightPupil.position.set(0, 0, 0.08);
    rightEye.add(rightPupil);

    // Mouth (Arc)
    const mouthCurve = new THREE.ArcCurve(0, 0, 0.5, Math.PI * 0.2, Math.PI * 0.8, false);
    const mouthPoints = mouthCurve.getPoints(20);
    const mouthGeometry = new THREE.BufferGeometry().setFromPoints(mouthPoints);
    const mouthMaterial = new THREE.LineBasicMaterial({ color: 0x000000, linewidth: 3 });
    mouth = new THREE.Line(mouthGeometry, mouthMaterial);
    mouth.position.set(0, -0.3, 0.9);
    avatar.add(mouth);

    // Start animation loop
    animate();

    // Socket.IO listener for speech
    const socket = io();
    socket.on('response', (data) => {
        speak(data.text);
        setEmotion(data.emotion || 'happy');
    });

    // Click to open dashboard
    renderer.domElement.addEventListener('click', () => {
        window.open('/', '_blank');
    });
}

// Lip-Sync Animation
function speak(text) {
    isSpeaking = true;
    const words = text.split(' ').length;
    const duration = Math.max(1, words * 0.3); // 300ms per word
    let elapsed = 0;
    const interval = setInterval(() => {
        elapsed += 0.05;
        const openness = Math.sin(elapsed * 20) * 0.3 + 0.3;
        updateMouth(openness);
        if (elapsed >= duration) {
            clearInterval(interval);
            isSpeaking = false;
            updateMouth(0);
        }
    }, 50);
}

// Update Mouth Shape
function updateMouth(openness) {
    const curve = new THREE.ArcCurve(0, 0, 0.5, Math.PI * (0.2 - openness), Math.PI * (0.8 + openness), false);
    const points = curve.getPoints(20);
    mouth.geometry.setFromPoints(points);
}

// Set Emotion (Eyes + Color)
function setEmotion(emo) {
    emotion = emo;
    const head = avatar.material;
    const colors = {
        'happy': 0x4a90e2,
        'sad': 0x95a5a6,
        'stressed': 0xe74c3c,
        'calm': 0x27ae60,
        'neutral': 0x9b59b6
    };
    head.color.setHex(colors[emo] || 0x4a90e2);

    // Eye blink for happy
    if (emo === 'happy') {
        eyes.scale.y = 0.8;
        setTimeout(() => { eyes.scale.y = 1; }, 200);
    }
}

// Floating Animation
function floatAvatar() {
    floatOffset += 0.02;
    avatar.position.y = Math.sin(floatOffset) * 0.1;
    avatar.rotation.y = Math.sin(floatOffset * 0.5) * 0.1;
}

// Animation Loop
function animate() {
    requestAnimationFrame(animate);
    floatAvatar();
    renderer.render(scene, camera);
}

// Responsive Resize
window.addEventListener('resize', () => {
    camera.aspect = 200 / 200;
    camera.updateProjectionMatrix();
    renderer.setSize(200, 200);
});

// Load Three.js dynamically
function loadThreeJS() {
    const script = document.createElement('script');
    script.src = 'https://cdn.jsdelivr.net/npm/three@0.152.0/build/three.min.js';
    script.onload = initAvatar;
    document.head.appendChild(script);
}

// Start
loadThreeJS();