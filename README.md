# GeoBox

Generate a geofeed file, straight from your netbox data!

GeoBox is a tiny python script that lets you generate [RFC8805](https://www.rfc-editor.org/rfc/rfc8805) geofeed.csv
files straight from your [netbox](https://github.com/netbox-community/netbox) data, allowing you to automate your
geofeed maintenance and to keep netbox as a source of truth for IP data.

## Setup instructions

- Make sure you have Python 3 (and pip3) installed.
- Clone this repository and install the dependencies:
  ```bash
  git clone https://github.com/FrumentumNL/GeoBox.git geobox
  cd geobox
  pip3 install -r requirements.txt
  ```
- Open your netbox installation, go to the customization tab and import the following files (in order):
    - **Custom Field Choices:** [choices.json](fields/choices.json)
    - **Custom Fields:** [fields.json](fields/fields.json)
  > [!NOTE]
  > Importing these files is currently broken due to a bug in netbox. This should be fixed in the next release. For now,
  > try taking a look at their contents to see the format.
- Create a new API key in netbox. It does not need write permissions.

Now, you can run the script!

```bash
# python3 geobox.py [installation url] [api key] [output location]
python3 geobox.py https://my.netbox.installation my_key /var/www/geofeed.csv
```
