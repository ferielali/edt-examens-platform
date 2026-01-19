# 🚀 EXACT STEP BY STEP INSTALLATION GUIDE

Follow these steps EXACTLY. Do not skip any step.

---

## PART 1: INSTALL REQUIRED SOFTWARE

### Step 1.1: Install Node.js
1. Open browser
2. Go to: https://nodejs.org/
3. Click the GREEN button (LTS version)
4. Run the downloaded file
5. Click "Next" → "Next" → "Next" → "Install"
6. Click "Finish"

### Step 1.2: Install Python
1. Go to: https://www.python.org/downloads/
2. Click "Download Python 3.x.x"
3. Run the downloaded file
4. ⚠️ **IMPORTANT**: Check ✅ "Add Python to PATH" at the bottom!
5. Click "Install Now"
6. Click "Close"

### Step 1.3: Install PostgreSQL
1. Go to: https://www.postgresql.org/download/windows/
2. Click "Download the installer"
3. Choose the latest version (Windows x86-64)
4. Run the downloaded file
5. Click "Next" → "Next" → "Next"
6. **IMPORTANT**: Enter a password (example: `admin123`)
7. ⚠️ **WRITE DOWN THIS PASSWORD!** You will need it later
8. Click "Next" → "Next" → "Next" → "Finish"

---

## PART 2: CREATE THE DATABASE

### Step 2.1: Open pgAdmin
1. Click Windows Start button
2. Type: `pgAdmin`
3. Click on "pgAdmin 4"
4. Wait for it to open (may take 30 seconds)
5. It will ask for a password → Enter any password you want (this is for pgAdmin only)

### Step 2.2: Connect to PostgreSQL
1. On the left side, click the arrow ▶ next to "Servers"
2. Double-click on "PostgreSQL XX"
3. Enter the password you created in Step 1.3
4. Click "OK"

### Step 2.3: Create the Database
1. Right-click on "Databases"
2. Click "Create" → "Database..."
3. In "Database" field, type: `exam_scheduler`
4. Click "Save"
5. You should see "exam_scheduler" in the list now ✅

### Step 2.4: Import the Data
1. Click on "exam_scheduler" (the database you just created)
2. Right-click on "exam_scheduler"
3. Click "Query Tool"
4. A new window opens with a text area
5. Click the 📁 folder icon (Open File) at the top
6. Navigate to: `[project folder]/database/full_backup.sql`
7. Click "Open"
8. You will see lots of SQL code appear
9. Click the ▶️ play button (Execute)
10. Wait... this may take 1-2 minutes
11. When done, you will see "Query returned successfully" at the bottom ✅

---

## PART 3: CONFIGURE THE BACKEND

### Step 3.1: Create the .env file
1. Open File Explorer
2. Go to the project folder → `backend`
3. Find the file named `.env.example`
4. Right-click on it → "Copy"
5. Right-click in empty space → "Paste"
6. You now have `.env.example - Copy`
7. Right-click on `.env.example - Copy` → "Rename"
8. Change the name to: `.env` (just .env, nothing else)
9. Click "Yes" if Windows warns you about changing extension

### Step 3.2: Edit the .env file
1. Right-click on `.env`
2. Click "Open with" → "Notepad"
3. Find this line:
   ```
   DATABASE_URL=postgresql://postgres:aboubakar@localhost:5432/exam_scheduler
   ```
4. Change `aboubakar` to YOUR PostgreSQL password (from Step 1.3)
   Example: If your password is `admin123`, change it to:
   ```
   DATABASE_URL=postgresql://postgres:admin123@localhost:5432/exam_scheduler
   ```
5. Press Ctrl+S to save
6. Close Notepad

---

## PART 4: INSTALL DEPENDENCIES

### Step 4.1: Open PowerShell
1. Open File Explorer
2. Go to the project folder
3. Click on the address bar at the top
4. Type: `powershell`
5. Press Enter
6. A blue/black PowerShell window opens

### Step 4.2: Install Backend Dependencies
Type these commands ONE BY ONE (press Enter after each):

```
cd backend
```

```
python -m venv venv
```

```
.\venv\Scripts\activate
```

(You should see `(venv)` at the beginning of the line now)

```
pip install -r requirements.txt
```

Wait for it to finish (may take 2-3 minutes)

### Step 4.3: Install Frontend Dependencies
1. Open ANOTHER PowerShell window (same way as Step 4.1)
2. Type these commands:

```
cd frontend
```

```
npm install
```

Wait for it to finish (may take 2-3 minutes)

---

## PART 5: RUN THE PROJECT

### Step 5.1: Start the Backend
In the FIRST PowerShell window (backend folder), type:

```
.\venv\Scripts\activate
```

```
python -m uvicorn app.main:app --reload --port 8000
```

You should see:
```
INFO:     Uvicorn running on http://127.0.0.1:8000
INFO:     Application startup complete.
```

⚠️ **DO NOT CLOSE THIS WINDOW!** Keep it open.

### Step 5.2: Start the Frontend
In the SECOND PowerShell window (frontend folder), type:

```
npm run dev
```

You should see:
```
VITE ready in XXX ms
➜  Local:   http://localhost:3000/
```

⚠️ **DO NOT CLOSE THIS WINDOW!** Keep it open.

---

## PART 6: OPEN THE APPLICATION

### Step 6.1: Open Browser
1. Open Google Chrome (or any browser)
2. In the address bar, type: `http://localhost:3000`
3. Press Enter

### Step 6.2: Login
Use these credentials:
- **Email**: `admin@univ.edu`
- **Password**: `admin123`

Click "Se connecter" (Login)

---

## 🎉 CONGRATULATIONS! THE PROJECT IS NOW RUNNING!

---

## ❌ TROUBLESHOOTING

### Problem: "psql is not recognized"
- Solution: Use pgAdmin instead (graphical interface)

### Problem: "Connection refused to database"
- Check PostgreSQL is running (search "Services" in Windows, find PostgreSQL)
- Check password in `.env` file is correct

### Problem: "npm is not recognized"
- Restart your computer after installing Node.js
- OR reinstall Node.js and make sure to check "Add to PATH"

### Problem: "python is not recognized"
- Reinstall Python and check ✅ "Add Python to PATH"

### Problem: Page shows error
- Make sure BOTH terminals are running (backend AND frontend)
- Check backend terminal for error messages

---

## 📞 NEED HELP?

If something doesn't work, send a screenshot of the error message!
