---
name: Bug report
about: Report a bug
title: ''
labels: ''
assignees: ''

---

**Before reporting the bug**
- [ ] I have looked at existing issues and none solved my problem
- [ ] I have installed the [tuxedo_keyboard driver](https://github.com/tuxedocomputers/tuxedo-keyboard) and rebooted
- [ ] I have made sure my laptop model is a TUXEDO / Clevo computer or derivative

**Describe the bug**
A clear and concise description of what the bug is: did it occur on a specific action? did you run tuxedo-backlight-control using the CLI (`backlight ui`) or the UI directly?
```bash
<Paste console output of the Tuxedo Backlight Control bug>
```

**Describe your OS environment**
* tuxedo-backlight-control version:  (run `backlight --version` and paste the result here)
* Python version: (run `python --version` and paste the result here)
* OS details:
  ```
  <run command "hostnamectl" (or "cat /etc/os-release") and paste the result here>
  ```
* tuxedo_keyboard SysFS folder is correctly installed:
  ```
  <run command "ls /sys/devices/platform/tuxedo_keyboard" and paste the result here>
  ```

**Additional context**
Add any other context about the problem here.
