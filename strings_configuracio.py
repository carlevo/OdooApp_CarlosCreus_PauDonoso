import os

class StringsConfiguracio:
    
    # Connexió a la base de dades de Render des de pgAdmin4
    # =====================================================
    # A pgAdmin4, per connectar-se a Render, fer servir com a hostname
    #       el de l'External Database URL
    #       postgresql://flask_postgres2526_pltj_user:AzMrQ9mnYHh2k3T90WSoVpjo8GiTbXpZ@dpg-d6k5s67pm1nc73e0df5g-a.frankfurt-postgres.render.com/flask_postgres2526_pltj
    #   Però sense el postgresql://, ni la part de l'usuari ni del 
    #   password, ni la part del final del nom de la base de dades.
    #   El que s'ha de posar en el camp "Host name/address" és:
    #      dpg-d6k5s67pm1nc73e0df5g-a.frankfurt-postgres.render.com
    nom_usuari = "flaskpostgres2625_user"
    password_usuari = "gzdWUsQkiQ4bmGG8oOCViTVMnb3TRWb5"
    uri_host = "dpg-d6tc6sh4tr6s739h4st0-a.frankfurt-postgres.render.com"
    port = "5432"
    nom_bd = "flaskpostgres2625"

    url_bd_online = f"postgresql://{nom_usuari}:{password_usuari}@{uri_host}:{port}/{nom_bd}?sslmode=require"
    # sslmode=require:
    #   SSL: Secure Sockets Layer. És el que fa servir Internet en general com a mesura de seguretat.
    #       Actualment, es fa servir no el SSL, sinó el TLS, que és una mesura més moderna i més segura 
    #       que el SSL. El nom SSL s'ha mantingut per tradició.
    #       El que fa és encriptar les dades que s'envien o es reben (entre el host i el client).
    #           Si s'utilitza en un navegador, en la ruta, comença per https://, si no, comença per http://.
    #
    #               En el cas de la url per connectar-nos amb la BD online, cal posar-ho, perquè sortim a Internet
    #                   i Render ho fa servir.
    #
    #               En el cas de la BD local, no cal posar-ho, perquè és local. A més, al ser local, quan es crea 
    #                   la BD, es crea sense aquesta opció per defecte. Per tant, si des del codi la posem, donarà 
    #                   error, a no ser que l'habilitem per la BD local (però al ser local, no cal).
    #
    #               El fet de posar el sslmode=require, fa que el nostre programa li demani a la BD que ho tingui 
    #                   habilitat, si no, no s'hi connecta.


    # Versió amb BD local
    # ===================
    '''nom_usuari = "postgres"
    password_usuari = "123456"
    uri_host = "localhost"
    port = "5432"
    nom_bd = "sge_roca_2526"

    url_bd_local = f"postgresql://{nom_usuari}:{password_usuari}@{uri_host}:{port}/{nom_bd}"'''

    # URL: Uniform Resource Locator (per webs).
    # URI: Uniform Resource Identifier (identifica qualsevol recurs).

    # Ens connectem amb la BD local o online.
    # =======================================
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL",
        url_bd_online
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # És una opció de SQLAlchemy.
    # SQLAlchemy, per defecte, posa aquest valor a True. El que fa a True, és escoltar si hi ha algun 
    #   canvi en algun objecte de la BD (taules, vistes, ...). Si s'utilitza, consumeix molts recursos 
    #   del servidor de la BD. Es posaria a True si es volgués reaccionar als canvis automàticament, 
    #   per exemple, per crear un log de totes les accions realitzades per diferents usuaris.
    #       Si féssim una aplicació de chat, no el faríem servir perquè es col·lapsaria per masses 
    #       peticions. Per un chat (temps real) es faria servir els WebSockets (dependència Flask-SocketIO).

    SECRET_KEY = "SecretKey" # S'hauria de canviar per una string menys evident.
    # És una opció de Flask.
    #   És una clau que fa servir Flask per encriptar la informació dels usuaris de la web.
    #       La informació encriptada és referent a la sessió de l'usuari i les coockies de l'usuari.
    #       Cada navegador i SO guarda les coockies a una carpeta o altra (Flask ja sap on segosn cada cas).
    #       Amb això, flask manté la sessió d'usuari, i sap que és aquell usuari. Amb això, s'evita que 
    #       el client vagi a la carpeta on hi ha la coockie guardad, i la modifiqui (no pot, perquè el client 
    #       no sap quina és la SECRET_KEY).
