# ✋ Handwave  
**Command your presentation with ease**  

🚀 *A web application that lets you control Google Slides presentations through natural hand gestures.*  

---

## 🌟 Project Motivation  

This project was born from two simple but powerful questions:  
1. 🤔 How can we make controlling a presentation more engaging and natural, beyond traditional mouse clicks and keyboard shortcuts?  
2. 🌌 How can we control a presentation in alternative ways — even at a distance or in the dark?  

The answer led us to create **Handwave**, a web application that enables gesture-based interaction with **Google Slides**.  

With Handwave you can:  
- ⏩ Move forward and backward through slides  
- ✍️ Draw and write annotations directly on slides  
- 🧹 Erase annotations  
- 📺 Toggle full-screen mode  
- 📂 Open and close presentations  

---

## 🖥️ Modes of Interaction  

Handwave offers **two control modes** to adapt to different environments:  

### 1️⃣ Webcam Mode  
- Uses the computer’s webcam to recognize hand gestures ✋  
- Enables **drawing and annotations** directly on slides  
- Best suited for **short/medium distances** from the computer  
- ⚠️ Requires **good lighting conditions** (not always guaranteed in conferences with projectors)  

### 2️⃣ Wio Terminal Mode  
- Uses a **microcontroller (Wio Terminal) with an accelerometer** 📡  
- Allows gesture control **even at a distance** and **in the dark** 🌑  
- ❌ Does not support the annotation feature  

---

## 🧩 Development Process  

### 🔍 Need Finding  
Our first step was to understand users’ needs and expectations for gesture-controlled presentations.  
We conducted **interviews and questionnaires** to collect insights.  

#### Key Questions Included:  
- 👥 Generational and usage context of the user  
- 📊 Last time the user presented slides and in which context  
- 🎯 Crucial actions for controlling a presentation  
- 😊 Positive and negative past experiences with similar technologies  
- 🔒 Privacy concerns: webcam vs. physical device  
- 💡 Willingness to use a gesture-based web application  

---

## 👥 Participants  

- **Interviews:** 17 participants (9 men, 8 women), aged **15–59 years**  
- **Questionnaires:** 115 responses (106 Italians, 9 internationals), 66 men and 49 women  
- Most respondents aged **25–35 years**  

---

## 📊 Key Findings  

- ✅ Most important actions:  
  - Navigating slides (forward/backward)  
  - Annotating on slides  
  - Entering full-screen mode  
  - Opening/closing the presentation  

- 🔒 Privacy:  
  - Most users had **no concern** with webcam usage  
  - Some worried about possible **data storage from the camera**  

- ⚖️ Preference:  
  - No clear preference between **camera-based** or **physical device-based** gesture recognition  
  - Many participants highlighted **advantages and disadvantages** of both approaches  
  - This motivated us to implement **both modes of interaction**, letting users choose the best option depending on the context  

---

## 🛠️ Implemented Tasks  

The following core features were implemented to meet user needs:  

- ⏩ Next slide  
- ⏪ Previous slide  
- ✍️ Annotate (draw) on slides  
- 🧹 Erase annotations  
- 📺 Full-screen mode  
- 📂 Open and load presentation  
- ❌ Close presentation  

Each task was visualized with a **storyboard** for clarity.  

---

## 📝 Design & Prototyping  

Once the main tasks were identified, we moved to **interface design**.  
To quickly test and refine our ideas, we used:  

- 📄 **Paper Prototyping**  
- 🔄 **Iterative testing** with user feedback  

This process allowed us to **gradually improve** the interface design, ensuring it was intuitive and user-friendly.  

---
