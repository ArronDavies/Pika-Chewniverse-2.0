import asyncio
import configparser
import threading
import os

def install():
    os.system('cmd /c "pip install -r requirements.txt"')

try:
    import Logger
except:
    print("No config has been generated")
    print("Generating now")
    import Utils.GenerateConfig
    Utils.GenerateConfig.main()
finally:
    import Logger
try:
    from AuthServer.Auth import Auth
    from CLI import CLI
    from CharacterServer.Character import Character
    from ZoneServer.Zone import Zone
except:
    install()

if __name__ == "__main__":
    config = configparser.ConfigParser()
    config.read('config.ini')
    Logger.logmanage()

    world_dict = {}
    try:
        auth = Auth(bind_ip="0.0.0.0", port=1001, max_connections=32, incoming_password=b"3.25 ND1", ssl=None)
        char = Character(bind_ip="0.0.0.0", port=1002, max_connections=32, incoming_password=b"3.25 ND1", ssl=None)
    except OSError:
        print("Ports are occupied")
        exit()

    zones_to_open = [1100]
    try:
        for zone in zones_to_open:
            zone_info = config[str(zone)]
            world_dict[zone] = Zone(bind_ip="0.0.0.0", port=int(zone_info['Port']), max_connections=32,
                                    incoming_password=b"3.25 ND1", ssl=None, zone_id=str(zone))
    except OSError:
        for zone in zones_to_open:
            zone_info = config[str(zone)]
            if not os.path.lexists(zone_info['LUZ']):
                print("LUZ not found")
                exit()
            if not os.path.lexists(zone_info['LVL']):
                print("LUZ not found")
                exit()
            else:
                print("Ports are occupied")
                exit()




    cli = threading.Thread(target=CLI, args=(world_dict,))
    cli.start()

    loop = asyncio.get_event_loop()
    loop.run_forever()
    loop.close()
