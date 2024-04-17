import requests
from requests.auth import HTTPBasicAuth
from datetime import date


url = 'http://38.45.54.14:8089/rest'
username = 'qslapi'
password = 'qslapi$2024**'
headers = {"Content-Type": "application/json"}

#Logica de la lista para verificar y bloquear
def desactivar(ip,val):
    ip=str(ip)

    if val==1:
        data = {"disabled": "false"}
        #leer la ip  y obtener la ID
        response = requests.get(
            url+'/ip/firewall/address-list?address='+ip, auth=HTTPBasicAuth(username, password),
            verify=False, headers=headers, json=data)

        if len(response.json()) != 0:
            #si ya existe unicamente actualiza
            for i in  response.json():
                j=list({i[".id"]})
                # print(j)
                actualizarStatus(j,1)
            # response = requests.patch(
            #     url+'/ip/firewall/address-list/'+j[0], auth=HTTPBasicAuth(username, password),
            #     verify=False, headers=headers, json=data)
            # print(response.json())
        else:
        #si el json viene vacio procede a crear el registro en el AL del firewall
            put(ip)
        #Recepcion de error 404 se ejecuta la siguiente sentencia
        # para registrar la regla
        if response.status_code == 404:
            put(ip)

    elif(val==2):

        response = requests.get(
            url+'/ip/firewall/address-list?address='+ip, auth=HTTPBasicAuth(username, password),
            verify=False, headers=headers)
        # print(response.json())
        for i in  response.json():
            j=list({i[".id"]})
            actualizarStatus(j,2)  

        # print(response.json())
#Buscador de rif en tabla Queue
def bRIF(rif,sta):
    #Buscador de rif en tabla Queue (Y CAMBIO DE STATUS)
    # if (sta != 0):
    
    response = requests.get(url+'/queue/simple?.proplist=target,name', auth=HTTPBasicAuth(username, password), verify=False)
    for i in response.json():
        val= str({i["name"]})
        posi=val.find(rif)
        if posi != -1:
            target = str({i["target"]})
            cadena = target.replace('{', '').replace('}', '').replace('"', '').replace('"','').replace("'",'')
            substrings = cadena.split(',')
            lista = [s.strip() for s in substrings]
            for i in lista:
                val=i[:-3]
                # print(i[:-3])
                if (sta!=0):
                    desactivar(val,sta)
                else:
                    return posi    
        
# Actualizador de status en tabla address List del firewall
def put(ip):
    #Agregar Ip a politica del firewall
    coment=f'bloqueado el: {date.today()}'
    data={
            "address": ip,
            "disabled": "false",
            "dynamic": "false",
            "comment" : coment,
            "list": "BLOCKED_USERS"
            }
    
    response = requests.put(
    url+'/ip/firewall/address-list', auth=HTTPBasicAuth(username, password),
    verify=False, headers=headers, json=data)
    #print(response.json())
# cambia el status y agrega la fecha de corte
def actualizarStatus(id,v):
    #se cambia el status de
    if v==1:
        
        coment= f'bloqueado el: {date.today()}'
        data = {"disabled": "false",
                "comment" : coment
                }
    else:
        coment= f'desbloqueado el: {date.today()}'
        data = {"disabled": "true",
                "comment" : coment
                }
    response = requests.patch(
    url+'/ip/firewall/address-list/'+id[0], auth=HTTPBasicAuth(username, password),
    verify=False, headers=headers, json=data)
    # print(response.json())

def addCliente(iden, rif, fecha_r,tipo ,cap):
    
    if (bRIF(rif,0)== None):
        rif=rif.upper()
        iden=iden.upper()
        cliente={
            "name": f"{fecha_r};{rif};\"{iden};{tipo} {cap};AVL",
            "queue": "default-small/default-small",
            "limit-at": "20000000/20000000",
            "max-limit": "20000000/20000000",
            "comment":"********Nuevo*Completar IP********",
            "target": "0.0.0.0"
        }

        response = requests.put(
        url+'/queue/simple', auth=HTTPBasicAuth(username, password),
        verify=False, headers=headers, json=cliente)
        
        return ("Creado")
        # print(response.json())
    else:
        return( "ya existe")
    
    

    ##agregar funcion de actualizacion de planes

#bRIF("rif",1 o 2 status)
addCliente("roberto compan c.a","J-11111111-3",date.today(),"DED","50")
# bRIF("J-11111111-9")

