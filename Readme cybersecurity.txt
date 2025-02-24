README File
Securing User Browsing: Comparing Browsers and Extensions Effectiveness against XSS Attacks
Team Members: Anmol Singhal, Ishit Vasoya

Video Presentation Link: https://olucdenver-my.sharepoint.com/:v:/g/personal/anmol_singhal_ucdenver_edu/ETz4Ay-fXslBhXW-CWwYRjUBQrndhOJh6AIR0N5zfPi3oQ?e=OY5mWx

PowerPoint Presentation Link: https://olucdenver-my.sharepoint.com/:p:/g/personal/anmol_singhal_ucdenver_edu/Efb7rcCKa2tCk0G0CgtOi74BhikN72pQk8-YL4NN-vUpqg?e=37woz3

Program Description:
This project aims to evaluate the effectiveness of different browser configurations in mitigating Cross-Site Scripting (XSS) attacks. The primary goal is to empirically decide which browser configurations offer the most robust defense against reflected XSS attacks. The assessment involves comprehensive testing of browsers with and without extensions, as well as an examination of the impact of Content Security Policy (CSP) headers implemented on target websites. The goal to show the user's which broswer is safe in mitigating XSS attack either without extension or with extensions or with CSP.

Project Details:
- The website is built using HTML, CSS, and Python for the backend.
- @ websites one with CSP and one without.
- User data is stored in .txt files.
- Uploaded files are stored in individual user directories.
- New code snippets are stored in a separate .txt file.
- A dedicated .txt file is used to manage all uploaded URLs.

Setup Directions:
1. Install Python from the official website: https://www.python.org/downloads/
   - Download the executable file and double-click to install.
   - Verify the installation by running `python --version` or `python3 --version` in the terminal. If a version number is displayed (e.g., x.xx.x), Python is installed successfully.
2. Install Flask using the pip command: `pip install Flask`
3. Install Flask-Session: `pip install flask-session`
4. Install Werkzeug: `pip install Werkzeug`

Usage:
1. Navigate to the project directory.(This could either be the website with Content security Policy or without CSP).
2. Open a terminal or command prompt in the project directory.
3. Run the command: `python app.py` (or `python3 app.py` on Linux).
4. The Flask application will start running, and you will see the URL where the website is hosted (e.g., http://127.0.0.1:5000).
5. Copy and paste the URL into your web browser to access the login page.

Attack Description:
This website has 5 vulnerabilities that can be exploited to perform XSS attacks:

Attack1.html is the file we will use for each file upload attack throughout the experiments. It has this code.
<script>
alert(document.cookie)
</script>

Attack1: File Upload: Once the file uploads it gives a URL, when we click this URL, it opens the file and malicious script is executed on the user’s system due to a lack of proper control and sanitization.

Attack2: URL: If you go to login page and add this script '? error=<script>alert ("Attack Happened”) </script>' in the URL or any other script where the current text of URL ends, and press enter the malicious script will be executed due to a lack of URL sanitization.

Attack3: Snippets: If you go to new snippets page and add script like <a onmouseover="alert(document.cookie)"> Hover around here...</a> in the text box, or any other script, and press submit, Post this if we go to my snippet page and hover on the text we will the malicious script is executed  due to a lack of input validation and sanitization.

Attack4: Text Box: If you go to update profile page and add script in the favorite color text box after writing the color blue' <a onmouseover="alert(document.cookie)"> and click on update and then go to dashboard.html page and Hover around where the favorite color blue is written, we will the malicious script is executed due to a lack of input validation and sanitization.

Attack5: Image: If you go to update profile page and add script in the First name text box after writing the name '<img src="notfound.png" onerror="alert('Congratulations, XSS attack')" and put any other image in profile picture make sure that the notfound.png does not exist click on update and then go to dashboard.html page and when you open the page there will be an error and you will see the malicious script is executed due to a lack of input validation and sanitization.

Attack3, 4 and 5 will the store those data into the database in this case .txt file and run every time when the pages is loaded,

Methodology:
- Two versions of the website were built: one without Content Security Policy (CSP) and one with CSP.
- The 5 attacks were tested on both websites across 6 different browsers (Chrome, Edge, Brave, Opera, Firefox, and Safari), one without extensions, one with extensions to mitigate attack and one with CSP.
- Extensions used: Chrome (CounterXSS, ScriptBlock), Edge (NoScript, Netcraft), Firefox (NoScript), Opera (Web Security Audit, ScriptSafe), Brave (NoScript, ScriptSafe). Safari had no extensions due to paid options.

Project Results:
- Without extensions and CSP, none of the 6 browsers were secure against even simple attacks.
- With CSP, all attacks were mitigated by all browsers, making the website safe.
- Netcraft, Web Security Audit, and CounterXSS, which claim to mitigate JavaScript code, did not work even against attacks with script tags.
- NoScript, supported by most browsers, mitigated all attacks on Brave, Edge, and Firefox. However, on Firefox, the URL attack showed a special warning, making NoScript work best on Firefox.
- Chrome's ScriptBlock and Brave's NoScript and ScriptSafe performed well.
- Safari iOS claims to be the most secure browser, but without extensions and CSP, all attacks were successful, refuting its security claims.Moreover available extensions were limited and paid.


In case of any issues with any of the links or the video and presentation quality or any clarity need please find below the contact details.
Contact Information
Anmol Singhal – anmol.singhal@ucdenver.edu 
Ishit Vasoya - ishitdilipbhai.vasoya@ucdenver.edu
