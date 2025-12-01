# 🌐 Share Your Project Using Ngrok (5 Minutes)

This guide shows you how to share your running project with anyone in the world using ngrok - **they only need a web browser!**

---

## ✅ What This Does

- ✅ Your colleague can access your project from anywhere
- ✅ They don't need to install Python, Docker, Ollama, or anything
- ✅ They just open a URL in their browser
- ✅ All processing happens on YOUR computer
- ✅ Setup takes 5 minutes

---

## 📥 Step 1: Install Ngrok

### Windows (Easiest):

**Option A: Direct Download**
1. Go to [ngrok.com/download](https://ngrok.com/download)
2. Download `ngrok-v3-stable-windows-amd64.zip`
3. Extract to a folder (e.g., `C:\ngrok\`)
4. Done!

**Option B: Using Chocolatey** (if you have it)
```bash
choco install ngrok
```

### Verify Installation:
```bash
ngrok version
```

---

## 🔑 Step 2: Sign Up (Free Account)

1. Go to [ngrok.com/signup](https://ngrok.com/signup)
2. Sign up (free - no credit card needed)
3. Copy your **authtoken** from the dashboard

---

## 🔧 Step 3: Configure Ngrok

Run this command **once** (replace with your actual token):

```bash
ngrok config add-authtoken YOUR_AUTH_TOKEN_HERE
```

Example:
```bash
ngrok config add-authtoken 2abc123def456ghi789jkl
```

---

## 🚀 Step 4: Start Your Project

Open a terminal and start your app as usual:

```bash
run_app.bat
```

Wait until you see:
```
You can now view your Streamlit app in your browser.
Local URL: http://localhost:8501
```

**Keep this terminal open!**

---

## 🌍 Step 5: Start Ngrok Tunnel

Open a **NEW terminal** (keep the first one running) and run:

```bash
ngrok http 8501
```

You'll see something like this:

```
ngrok

Session Status                online
Account                       your-email@example.com
Version                       3.x.x
Region                        United States (us)
Latency                       -
Web Interface                 http://127.0.0.1:4040
Forwarding                    https://abc123.ngrok-free.app -> http://localhost:8501

Connections                   ttl     opn     rt1     rt5     p50     p90
                              0       0       0.00    0.00    0.00    0.00
```

---

## 📤 Step 6: Share the URL

**Copy the HTTPS URL** (e.g., `https://abc123.ngrok-free.app`)

Send this URL to your colleague via:
- Email
- WhatsApp
- Slack
- Any messaging app

They can open it in their browser immediately!

---

## 🎯 What Your Colleague Sees

1. They open the URL in their browser
2. They see a ngrok warning page (click "Visit Site")
3. They see your Streamlit app - fully functional!
4. They can:
   - Upload CSV files
   - Run analysis
   - View dashboards
   - Use the chat interface

**All processing happens on YOUR computer!**

---

## 🛑 Stopping the Share

When you're done:

1. **Stop ngrok**: Press `Ctrl+C` in the ngrok terminal
2. **Stop your app**: Press `Ctrl+C` in the Streamlit terminal
3. The URL will stop working immediately

---

## 💡 Important Notes

### ✅ Advantages:
- **Zero setup** for your colleague
- **Works from anywhere** (different country, different network)
- **Free tier** is sufficient for demos
- **Secure HTTPS** connection

### ⚠️ Limitations (Free Tier):
- **URL changes** every time you restart ngrok
- **Session timeout** after 2 hours (just restart)
- **Limited bandwidth** (fine for 1-5 users)
- **Ngrok warning page** (visitors must click "Visit Site")

### 🔒 Security:
- Only share the URL with people you trust
- Anyone with the URL can access your app
- Stop ngrok when not in use

---

## 🎨 Better Experience (Optional)

### Remove Ngrok Warning Page ($8/month):

Upgrade to ngrok paid plan to get:
- **Fixed domain** (e.g., `your-app.ngrok.app`)
- **No warning page**
- **Longer sessions**
- **More bandwidth**

---

## 📝 Quick Reference

### Start Everything:

**Terminal 1:**
```bash
docker-compose up -d
run_app.bat
```

**Terminal 2:**
```bash
ngrok http 8501
```

### Stop Everything:

**Terminal 2:**
```bash
Ctrl+C  # Stop ngrok
```

**Terminal 1:**
```bash
Ctrl+C  # Stop Streamlit
docker-compose down  # Stop Docker
```

---

## 🔧 Troubleshooting

### Issue: "ngrok not found"

**Solution:**
Add ngrok to your PATH or use full path:
```bash
C:\ngrok\ngrok.exe http 8501
```

---

### Issue: "Failed to start tunnel"

**Solution:**
Make sure you added your authtoken:
```bash
ngrok config add-authtoken YOUR_TOKEN
```

---

### Issue: "Connection refused"

**Solution:**
Make sure Streamlit is running first:
```bash
# Check if app is running at http://localhost:8501
# Then start ngrok
```

---

### Issue: URL is slow for colleague

**Solution:**
This is normal - data travels through ngrok servers. For better performance:
- Use ngrok paid plan (faster servers)
- Or deploy to cloud (AWS/DigitalOcean)

---

## 🎉 Success Checklist

- ✅ Ngrok installed
- ✅ Authtoken configured
- ✅ Streamlit app running on localhost:8501
- ✅ Ngrok tunnel active
- ✅ HTTPS URL copied
- ✅ Colleague can access the URL
- ✅ App works in their browser

---

## 🆚 Ngrok vs Other Options

| Method | Setup Time | Cost | Colleague Needs |
|--------|------------|------|-----------------|
| **Ngrok** | 5 min | Free | Just a browser |
| **Send Code** | 30 min | Free | Install everything |
| **Cloud Deploy** | 2 hours | $15-30/mo | Just a browser |

**For showing/demoing: Ngrok is the best choice! 🎯**

---

## 📞 Example Conversation

**You:** "Hey, check out my project at https://abc123.ngrok-free.app"

**Colleague:** "Cool! I can see it. Let me try uploading a file..."

**You:** "Go ahead! Everything runs on my machine, so it should be fast."

**Colleague:** "Wow, this is amazing! The analysis is so detailed!"

---

**That's it! Happy sharing! 🚀**
