/* ==== GLOBAL STYLES ==== */
* {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
}

body {
  font-family: "Segoe UI", Arial, sans-serif;
  background-color: #f4f6f8;
  color: #333;
  padding: 20px;
}

/* ==== DASHBOARD WRAPPER ==== */
.dashboard {
  max-width: 900px;
  margin: 0 auto;
  background-color: #fff;
  border-radius: 12px;
  padding: 25px 30px;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
  transition: box-shadow 0.3s ease;
}

.dashboard:hover {
  box-shadow: 0 6px 18px rgba(0, 0, 0, 0.15);
}

/* ==== HEADER ==== */
header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-bottom: 2px solid #e9ecef;
  padding-bottom: 10px;
}

header h1 {
  font-size: 1.5rem;
  color: #007bff;
  font-weight: 600;
}

/* ==== STATUS INDICATOR ==== */
.status {
  font-size: 0.9rem;
  color: green;
  font-weight: 500;
}

/* ==== CHAT AREA ==== */
.chat-container {
  margin: 25px 0;
  display: flex;
  flex-direction: column;
  gap: 10px;
}

#chat {
  height: 350px;
  overflow-y: auto;
  border: 1px solid #ddd;
  padding: 12px;
  background-color: #fafafa;
  border-radius: 8px;
  scroll-behavior: smooth;
}

/* ==== MESSAGES ==== */
.message {
  margin: 8px 0;
  padding: 10px 12px;
  background-color: #e9ecef;
  border-radius: 8px;
  line-height: 1.5;
  font-size: 0.95rem;
  word-wrap: break-word;
  max-width: 80%;
}

.message strong {
  color: #007bff;
}

.message.user {
  background-color: #007bff;
  color: #fff;
  align-self: flex-end;
  margin-left: auto;
}

.message.bot {
  background-color: #e9ecef;
  color: #333;
  align-self: flex-start;
}

/* ==== INPUT + BUTTONS ==== */
#query {
  width: 70%;
  padding: 10px;
  font-size: 1rem;
  border: 1px solid #ccc;
  border-radius: 6px;
  outline: none;
  transition: border-color 0.3s ease;
}

#query:focus {
  border-color: #007bff;
}

button {
  padding: 10px 15px;
  background-color: #007bff;
  color: #fff;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  transition: background-color 0.3s ease, transform 0.1s ease;
}

button:hover {
  background-color: #0056b3;
  transform: scale(1.05);
}

/* ==== FEATURES SECTION ==== */
.features {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  margin-top: 15px;
}

.features button {
  background-color: #6c757d;
}

.features button:hover {
  background-color: #495057;
}

/* ==== FLOATING ASSISTANT BUBBLE ==== */
.bubble {
  position: fixed;
  bottom: 25px;
  right: 25px;
  background: linear-gradient(135deg, #007bff, #0056b3);
  color: #fff;
  padding: 15px 18px;
  border-radius: 50%;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3);
  z-index: 1000;
  font-weight: 500;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s ease;
  width: 60px;
  height: 60px;
}

.bubble:hover {
  transform: scale(1.1);
  background: linear-gradient(135deg, #0056b3, #00408a);
}

.hidden {
  display: none !important;
}

/* ==== TIMELINE ==== */
.timeline {
  margin-top: 20px;
  padding: 15px;
  background-color: #f1f3f5;
  border-radius: 8px;
  border: 1px solid #dee2e6;
}

.timeline h3 {
  margin-bottom: 10px;
  color: #007bff;
}

.event {
  padding: 8px;
  cursor: pointer;
  border-bottom: 1px solid #dee2e6;
  transition: background-color 0.3s ease, color 0.3s ease;
}

.event:last-child {
  border-bottom: none;
}

.event:hover {
  background-color: #007bff;
  color: #fff;
}

/* ==== SCROLLBAR STYLING ==== */
#chat::-webkit-scrollbar {
  width: 8px;
}

#chat::-webkit-scrollbar-thumb {
  background: #007bff;
  border-radius: 5px;
}

#chat::-webkit-scrollbar-track {
  background: #f1f1f1;
}

/* ==== RESPONSIVE DESIGN ==== */
@media (max-width: 768px) {
  .dashboard {
    padding: 20px;
  }

  header h1 {
    font-size: 1.25rem;
  }

  #query {
    width: 100%;
    margin-bottom: 10px;
  }

  .bubble {
    bottom: 15px;
    right: 15px;
    width: 50px;
    height: 50px;
    padding: 12px;
  }
}
