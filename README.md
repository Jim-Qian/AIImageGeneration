https://jimdemo.online/

**Steps for starting this website (no debugging locally):**  
source env/bin/activate                                                ->  Enable local Python environment  

Frontend/npm run dev                                                   ->  Runs Frontend  
Backend/redis-server                                                   ->  Runs Redis Server  
PYTHONPATH=Backend FLASK_APP=controller2 flask run --host=localhost    ->  Runs Backend (use this command directly in project folder)                                   

**Steps for starting this website (debugging locally):**  
1. Same as above do for all parts you are not debugging.  
2. Comment out all portions except the 1 you are debugging in ".vscode/launch.json".  
3. Start VS Code.

**Steps for starting this website (on cloud for HTTPS):**
1. Rent a domain (example.com)
2. Rent a cloud instance. Open its 443 and 80 port.
3. Add 2 A records to that domain using DNS: 1 for "www.example.com" and 1 for "example.com". Both to the public IP address of cloud instance.
  •  Double check using nslookup
4. Install and use Certbot to get HTTPS certificate for your website
5. Install, modify, and start Nginx (to serve HTTPS certificate)
6. Run all those above commands to start your own backend code. Do those with pm2 so they persist and can reboot when EC2 instance restarts. I recommend using a cloud host with 4GB of RAM (using 1GB shuts down pm2 and can't even allow ssh to it).

**Steps for pm2:**
1. cd /home/ec2-user/AIImageGeneration
2. pm2 start "npm run dev" --name Frontend --cwd ./Frontend
3. pm2 start ./Production/start-backend.sh --name Backend
4. pm2 start "redis-server" --name Redis
5. sudo env PATH=$PATH:/usr/bin /usr/lib/nodejs18/lib/node_modules/pm2/bin/pm2 startup systemd -u ec2-user --hp /home/ec2-user
6. pm2 save

------

**Steps on how this website works (localhost):**  
1. Browser goes to localhost:3000. Gets served generated HTML and CSS and Javascript built from ts, tsx, and css by Next.js.  
2. When browser clicks on a button, for example "Login", the browser sends a JSON POST request to ( localhost:3000/api/login ) (along with any cookie), which then triggers the Next.js server to send a request to ( localhost:5000 ).  
  - The browser never directly communicates with Flask - it always goes through the Next.js proxy first.  
3. Flask sends a response back to :3000 to the Next.js server, not to the browser directly. Then Next.js server sends to the browser (including any cookie).  
Browser never talk directly with :5000.  

Next.js server - Not part of the Frontend browser. It is also a proxy.  
  •  Deployed on Vercel/AWS/...  
  •  Serves HTML/CSS/JS to users  
  •  Handles API routes  
  •  Runs on mywebsite.com  
Flask server  
  •  Deployed on AWS/Heroku/...  
  •  Handles database/business logic  
  •  Runs on api.mywebsite.com  

Browser (origin: localhost:3000)  
  ↓ Request to same origin (localhost:3000/api/login)  
Next.js Server (origin: localhost:3000) ✅ SAME ORIGIN = NO CORS ISSUES  
  ↓ Server-to-server request (not subject to CORS)  
Flask Server (origin: localhost:5000)  

During production, you host both the Next.js Server and the Flask Server in the cloud (in the same computer or different).  

------

**Frontend/ contains those folders created by Next.js**:  
```
Frontend/  
    app/  
        *api/  
            check-auth/  
                route.ts  
            login/  
                route.ts  
            logout/  
                route.ts  
            register/  
                route.ts  
        login/  
            page.tsx                   Login page  
        register/  
            page.tsx                   Register page  
        user/  
            page.tsx                   User page  
        *.../  
        globals.css      
        layout.tsx                     Shared UI across multiple pages. Includes <html> and <body>  
        page.tsx                       Home page  
    components/                        Reusable custom UI components. More .tsx files  
    hooks/                             Reusable custom React hooks  
    lib/                               Some helper function(s) in .ts file(s)  
    node_modules/  
    public/                            Currently empty  
    styles/                            CSSs  
```

Folder with * in front means you need to add new folders/files to create new pages in this website.  

Those page.tsx files include all the frontend logic (besides logic for hitting api which is placed within the api/ folder) and includes the "template html" in JSX format.  

When a user types ( yoursite.com/login ) in the browser:  
Browser → Next.js Router → app/login/page.tsx → Login() function executes  
  •  That function is automatically used by Next.js's App Router: you don't explicitly import or call it anywhere in your code.  
  •  If I want to create a new Next.js page for ( yoursite.com/another ), I just need to create "another" folder within app folder and place a page.tsx file within "another". And make sure that page.tsx looks similar to previous .tsx files provided by V0.  

------

**Also within Frontend/ are those 9 files**:  
NPM:  
package.json  
package-lock.json  

PNPM (another package manager):  
pnpm-lock.yaml  

CSS:  
postcss.config.mjs  
Tailwind CSS (https://ui.shadcn.com/):  
tailwind.config.ts  
components.json  

TS:  
tsconfig.json  

Next.js:  
next-env.d.ts  
next.config.mjs  
