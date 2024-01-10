# you may wonder why this is not just a file.
# the reason is that this loads faster and does not rquire a disk Access
# each time HTTP is accessed.

html = '''
<!DOCTYPE html>
<html lang="en">
<head>
  <!--<meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>APP</title> -->
  <style>
    body {
      background-color: #d5f4e6;     
    }
    table.leftright{
      border: 2px solid orange;
      border-collapse: collapse;   
    }
    th.leftright{
      text-align: center;
    }
    td.leftright{
      text-align: center;
    }
    table.center{
      border: 2px solid orange;
      border-collapse: collapse;
    }
    th.center{
      border: 2px solid orange;
      border-collapse: collapse;
      text-align: center;
    }
    td.center{
      border: 2px solid orange;
      border-collapse: collapse;
      text-align: center;
    }

    table td,tr{
      border: 2px solid blue;
      border-collapse: collapse; 
    } 
    
  </style>
</head>

<body>
  <table style="border: none;">
    <tr style="border: none;">
        <td style="border: none;"><h1  style="font-size: 40px;">home-broker:&nbsp&nbsp</h1></td>

        <td style="border: none;"><h2>Device and WeMo/fauxmo Management</h2></td>
    </tr>
  </table>
  <table>
    <tr>
      <th  style="text-align: left;">
        <a href="http://home-broker.local:8080/">
          <h2>Maintain zigbee2mqtt Devices</h2>
        </a>
        <h3 style="color: red" ;>{{error_message}}</h3>
      </th>
    </tr>
    <tr>
      <td>
        <form action="/create_wemo" method="post">
          <h2>WeMo to Device mapping</h2>
          <table class="leftright">
            <tr>
              <th>
                <button type="submit" name=action value="create_wemo">Create WeMo</button>
              </th>
              <th>
                <label for="wemo_name">WeMo Name:</label>
                <input type="text" id="wemo_name" name="wemo_name"><br>
                <label for="wemo_port">WeMo Port:</label>
                <input type="text" id="wemo_port" name="wemo_port" value="Optional"><br>
              </th>
              <th>
                Device:
              </th>
              <th>
                <select id="wemo_device" name="wemo_device" size="5">
                  {% for b in get_devices_for_wemo %}
                  <option value="{{b[0]}}">{{b[1]}}&nbsp[{{b[2]}}],&nbsp{{b[3]}}&nbsp[{{b[4]}}] </option>
                  {% endfor %}
                </select>
              </th>
              <th>
                <button type="submit" name=action value="restart">Restart FauxMo Process</button>
              </th>
            </tr>
          </table>
        </form>
      </td>
    </tr>

    <tr>
      <td>
        <form action="/modify_wemo" method="post">
          <table class="center">
            <tr>
              <th rowspan="2">
                Mapped WeMo
              </th>
              <th colspan="2">
                WeMo
              </th>
              <th colspan="100%">
                MQTT
              </th>
            </tr>
            <tr>
              <th>
                Name
              </th>
              <th>
                port
              </th>
              <th>
                Friendly Name
              </th>
              <th>
                Description
              </th>
              <th>
                feature
              </th>
              <th>
                on payload
              </th>
              <th>
                off payload
              </th>
            </tr>
            {% for d in all_wemo %}
            <tr>
              <td>
                <button type="submit" name=action value="delete_wemo/{{d[0]}}">Delete</button>
              </td>
              <td>{{d[1]}}</td>
              <td>{{d[2]}}</td>
              <td>{{d[3]}}</td>
              <td>{{d[4]}}</td>
              <td>{{d[5]}}</td>
              <td>{{d[6]}}</td>
              <td>{{d[7]}}</td>
            </tr>
            {% endfor %}
          </table>
        </form>
      </td>
    </tr>
    <tr>
      <td>
        <form action=" /create_IP_device" method="post">
          <h2>Manual Creation of IP Devices</h2>
          <table class="leftright">
            <tr>
              <td><button type="submit" name=action value="create_wifi">Create IP Device</button>
              <th><label for="IP_name">Device Name:</label>
                <input type="text" id="IP_name" name="IP_name"><br>
              </th>
              <th><label for="IP_description">Description:</label>
                <input type="text" id="IP_description" name="IP_description"><br>
              </th>
            </tr>
          </table>
        </form>
      </td>
    </tr>
    <tr>
      <td>
        <form action="/create_IP_feature" method="post">
          <table class="leftright">
            <tr>
              <td><button type="submit" name=action value="create_IP_feature">Create IP Device feature</button>
              <th><label for="wifi_access">Device Name:</label>
              <td>
                <select name="device_ieee_address" size="4">
                  {% for b in manual_device_names %}
                  <option value="{{b[0]}}">{{b[1]}}&nbsp[{{b[2]}}] </option>
                  {% endfor %}
                </select>
              </td>
              </th>
              <th><label for="property">property:</label>
                <input type="text" id="property" name="property"><br>
              </th>
            </tr>
          </table>
        </form>
      </td>
    </tr>
    {% if do_update_IP %}
    <tr>
      <td>
        <form action="/update_IP" method="post">
          <table class="leftright">
            <tr>
              <th>
                <button type="submit" name=action value="Update/{{man_ip[0]}}">Update</button><br>
                &nbsp;<br>
                <button type="submit" name=action value="Delete/{{man_ip[0]}}">Delete</button>
              </th>
              <th>
                <h1>[{{man_ip[2]}}]&nbsp[{{man_ip[3]}}]</h1>
              </th>
            </tr>
            <tr>
              <th>
                Feature Type
              </th>
              <td>
                <select name="type">
                  <option value="{{man_ip[4]}}">{{man_ip[4]}}</option>
                  <option value="binary">Binary</option>
                  <option value="numeric">Numeric</option>
                </select>
              </td>
            </tr>
            <tr>
              <th>
                MQTT set topic
              </th>
              <td>
                <input type="text" size="30" name="set_topic" value="{{man_ip[5]}}">
              </td>
            </tr>
            <tr>
              <th>
                Payload On/Numeric value
              </th>
              <td>
                <input type="text" size="30" name="on" value="{{man_ip[6]}}">
              </td>
            </tr>
            <tr>
              <th>
                Payload Off value
              </th>
              <td>
                <input type="text" size="30" name="off" value="{{man_ip[7]}}">
              </td>
            </tr>
            <tr>
              <th>
                MQTT get topic
              </th>
              <td>
                <input type="text" size="30" name="get_topic" value="{{man_ip[8]}}">
              </td>
            </tr>
            <tr>
              <th>
                Empty value
              </th>
              <td>
                <input type="text" size="30" name="empty" value="{{man_ip[9]}}">
              </td>
            </tr>
            <tr>
              <th>
                MQTT Subscribe topic
              </th>
              <td>
                <input type="text" size="30" name="pub_topic" value="{{man_ip[10]}}">
              </td>
            </tr>
          </table>
        </form>
      </td>
    </tr>
    {% endif %}
    </td>
    </tr>
    <tr>
      <td>
        <form action="/all_devices" method="post">
          <h2>All DEVICES (Manual IP, Auto IP, ZigBee)</h2>
          <table class="center">
            <tr>
              <th>
                ieee_address
              </th>
              <th>
                Friendly name
              </th>
              <th>
                Description
              </th>
              <th>
                last<br>date
              </th>
              <th>
                feature<br>property<br>Name
              </th>
              <th>
                feature<br>Description
              </th>
              <th>
                Type
              </th>
              <th>
                Access<br>Bits
              </th>
              <th>
                Set/publish topic
              </th>
              <th>
                Get topic
              </th>
              <th>
                Subscribe topic
              </th>
              <th>
                True<br>value
              </th>
              <th>
                False<br>value
              </th>
              <th>
                Empty<br>Get value
              </th>
            </tr>
            <tr>
              <th colspan="100%"  style="text-align: left;">Manual IP devices</th>
            </tr>
            {% for d in manIP_devices %}
            <tr>
              <td align="center">
                {{d[16]}} 
                {% if d[1] %}
                <button type="submit" name=action value="manIP/{{d[0]}}">Modify
                  values
                </button>
                <button type="submit" name=action value="delete/{{d[1]}}">
                    Delete
                </button>
                {% endif %}
              </td>
              <th>{{d[2]}}</th>
              <td>{{d[3]}}</td>
              <td>{{d[4]}}</td>
              <td>{{d[5]}}</td>
              <td>{{d[6]}}</td>
              <td>{{d[7]}}</td>
              <td>{{d[8]}}</td>
              <td>{{d[9]}}</td>
              <td>{{d[10]}}</td>
              <td>{{d[11]}}</td>
              <td>{{d[12]}}<br>{% if d[15] %} <button type="submit" name=action value="send/1/{{d[0]}}">Send</button>{%
                endif %}</td>
              <td>{{d[13]}}<br>{% if d[15] %} <button type="submit" name=action value="send/0/{{d[0]}}">Send</button>
                {%endif %}</td>
              <td>{{d[14]}}</td>
            </tr>
            {% endfor %}
            <tr>
              <th colspan="100%"  style="text-align: left;">Auto IP devices</th>
            </tr>
            {% for d in autoIP_devices %}
            <tr>
              <td>
                {{d[16]}}
                {% if d[1] %}
                <button type="submit" name=action value="delete/{{d[1]}}">
                  Delete
                </button>
                {% endif %}
              </td>
              <th>{{d[2]}}</th>
              <td>{{d[3]}}</td>
              <td>{{d[4]}}</td>
              <td>{{d[5]}}</td>
              <td>{{d[6]}}</td>
              <td>{{d[7]}}</td>
              <td>{{d[8]}}</td>
              <td>{{d[9]}}</td>
              <td>{{d[10]}}</td>
              <td>{{d[11]}}</td>
              <td>{{d[12]}}<br>{% if d[15] %} <button type="submit" name=action value="send/1/{{d[0]}}">Send</button>{%
                endif %}</td>
              <td>{{d[13]}}<br>{% if d[15] %} <button type="submit" name=action value="send/0/{{d[0]}}">Send</button>{%
                endif %}</td>
              <td>{{d[14]}}</td>
            </tr>
            {% endfor %}
            <tr>
              <th colspan="100%"  style="text-align: left;">ZigBee devices
                <button type="submit" name=action value="refresh/zigbee}">Refresh ZigBee2MQTT devices</button>
              </th>
            </tr>
            {% for d in zigbee_devices %}
            <tr>
              <td>{{d[16]}}</td>
              <th>{{d[2]}}</th>
              <td>{{d[3]}}</td>
              <td>{{d[4]}}</td>
              <td>{{d[5]}}</td>
              <td>{{d[6]}}</td>
              <td>{{d[7]}}</td>
              <td>{{d[8]}}</td>
              <td>{{d[9]}}</td>
              <td>{{d[10]}}</td>
              <td>{{d[11]}}</td>
              <td>{{d[12]}}<br>{% if d[15] %} <button type="submit" name=action value="send/1/{{d[0]}}">Send</button>{%
                endif %}</td>
              <td>{{d[13]}}<br>{% if d[15] %} <button type="submit" name=action value="send/0/{{d[0]}}">Send</button>{%
                endif %}</td>
              <td>{{d[14]}}</td>
            </tr>
            {% endfor %}
          </table>
        </form>
      </td>
    </tr>
  </table>
</body>

</html>
'''

if __name__ == "__main__":
    import os
    import webbrowser

    path = os.path.abspath('sample.html')
    print(path)
    url = 'file://' + path

    with open(path, 'w') as f:
      f.write(html)
    webbrowser.open(url)