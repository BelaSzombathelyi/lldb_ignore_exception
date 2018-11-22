# lldb_ignore_exception
iOS debug helpers


Prepare your .libinit file to collect heleper imports:
Create the file if needed
```
touch ~/.lldbinit
```
```
ecoh ~/.lldbinit << {YOUR_LOCAL_PATH} ignore_specified_objc_exceptions.py
```

![debug output on start](Images/'1.png')
