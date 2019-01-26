# e4-client
![build_badge](https://readthedocs.org/projects/e4-client/badge/?version=latest)

Client to download information of the E4 Connect platform.

## Installation
```sh 
$ pip install -r requeriments.txt
```

## Usage

```sh 
$ python emp-client.py [-h] [-u USER] [-p PWD] [-a] [-i SESSION_ID] [-l] [-o OUT]
```

&nbsp;&nbsp;&nbsp;&nbsp;**-h, --help**&nbsp;&nbsp;&nbsp;&nbsp;Help message

&nbsp;&nbsp;&nbsp;&nbsp;**-u USER, --user USER**&nbsp;&nbsp;&nbsp;&nbsp;Username.

&nbsp;&nbsp;&nbsp;&nbsp;**-p PWD, --pwd PWD**&nbsp;&nbsp;&nbsp;&nbsp;Password.

&nbsp;&nbsp;&nbsp;&nbsp;**-a, --all_sessions**&nbsp;&nbsp;&nbsp;&nbsp;Downloads all sessions of a user.

&nbsp;&nbsp;&nbsp;&nbsp;**-i SESSION_ID, --session_id SESSION_ID**&nbsp;&nbsp;&nbsp;&nbsp;Downloads a specific session.

&nbsp;&nbsp;&nbsp;&nbsp;**-l, --sessions_list**&nbsp;&nbsp;&nbsp;&nbsp;Downloads the list of sessions in CSV format. It includes the following columns: _id, device_id	duration, status, start_time, label	device, exit_code_.

&nbsp;&nbsp;&nbsp;&nbsp;**-p, --purchased_devs**&nbsp;&nbsp;&nbsp;&nbsp;Downloads the list of purchses devices in CSV format. It includes the following columns: _device_id, label, model, hardware_code, purchase_code, purchase_id_.

&nbsp;&nbsp;&nbsp;&nbsp;**-o OUT, --out OUT**&nbsp;&nbsp;&nbsp;&nbsp;Output file or path.

## Authentication through environment variables
The username and the password can also be specified using environment variables. In Linux they can be specified as follows:

```sh
$ export E4_USER=[username]
$ export E4_PWD=[password]
```

## Examples
` $ python3 emp-client.py -u e4user@mail.com -p pass -a -o out`

Downloads all the episodes in the _out_ folder.

` $ python3 emp-client.py -i 67677`

Downloads the episode that has 67677 as identifier. Since no credentials are specified, it is assumed that they are registered in the environment variables.

` $ python3 emp-client.py -l -o output.csv`

Downloads the list of episodes as a CSV (output.csv). 

` $ python3 emp-client.py -p`

Downloads the list of purchased devices. 

## Documentation
The E4 client can also be used as a library in external projects. The logic is encapsulated in the E4Connect class, that contain methods to retrieve the information of the platform. Documentation can be accessed [here](http://e4-client.readthedocs.io/).
