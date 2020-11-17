# H_task
> API will accept png/jpg images or pdf files
> Temporary convert first pdf page to image for future handling
> Perform text recognition in Russian language
> Image that was not recognised as document will return an error response
> Look for signature using algorithm depend on doc_type:
- Simple color masking on standard document with blue pen signature
- Use connected component analysis

>> API will return Json:
- with number int of signatures found
- image with masked out signatures
- recognised text

http://127.0.0.1:8000/api/doc/upload/

- 📂 __H\_dj\_task__
   - 📂 __api\_app__ (app for handling API and recognition documents)
     - 📂 __image\_parsing__
       - 📄 [img\_parse\_main.py](main file that build api response and text recognition function)
       - 📄 [sig\_recog.py](cv2 and scikit-image image handling)
     - 📄 [views.py](interface for API handeling)
   - 📂 __main\_app__ 
     - 📄 [models.py](All models in main app)
     - 📂 __tests__ 
   - 📂 __uploads__ (media files will be uploaded here)
   - 📂 __user\_app__ (app for handeling tokens and creating new users via API)
     - 📄 [views.py](interface for API handeling)

Everything else is serializers/urls and classical Django project without much changes.

|Info  | URL |
| ------ | ------ |
| POST: upload document and link it to user; Get: return uploaded documents by logged in user | [http://127.0.0.1:8000/api/doc/upload/] |
| POST:Create User | [http://127.0.0.1:8000/api/user/create/] |
| GET:Loged in user information  PUT: Edit user information | [http://127.0.0.1:8000/api/user/me/]
| POST:Create token for user | [http://127.0.0.1:8000/api/user/token/] |

### Docker and Docker-Compose

The Docker-compose will start django server on local host on port 8000. 
Warning.  If you want to rebuild docker that can take forever since there a lot of dependencies to compile.
