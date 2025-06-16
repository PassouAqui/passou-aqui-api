from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from django.contrib.auth.models import User
class RegisterView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        try:
            data = request.data
            first_name = data['first_name']
            last_name = data['last_name']
            username = data['username']
            password = data['password']
            re_password = data['re_password']

            if password == re_password:
                if len(password) >= 8:
                    if not User.objects.filter(username=username).exists:
                        user = User.create_user(
                            first_name = first_name,
                            last_name = last_name,
                            username = username,
                            password = password,
                            re_password = re_password,
                        )

                        user.save()
                        return Response({
                            'sucess': 'Conta criada com sucesso!'
                        },
                        status=status.HTTP_201_CREATED 
                        ),

                    else:
                        return Response({
                            'error': 'Username ja utilizado'
                        },
                        status=status.HTTP_400_BAD_REQUEST 
                        )

                else:
                    return Response({
                        'error': 'A senha é menor do que 8 caractéres'
                    },
                    status=status.HTTP_400_BAD_REQUEST 
                    )
            else: 
                return Response({
                    'error': 'As senhas não são iguais'
                },
                    status=status.HTTP_400_BAD_REQUEST 
                )
        
        except:
            return Response(
                {
                    "error:" : "erro ao criar conta"
                },
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )