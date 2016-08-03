#! /bin/sh -
#
# Install OpenVPN connections for all available
# regions to NetworkManager
#
# Requirements:
#   should be run as root
#   python and openvpn (will be installed if not present)
#
# Usage:
#  install [--version]

IFS='
	 '
SERVER_INFO=/tmp/server_info
SPLIT_TOKEN=':'

error( )
{
  echo "$@" 1>&2
  exit 1
}

error_and_usage( )
{
  echo "$@" 1>&2
  usage_and_exit 1
}

usage( )
{
  echo "Usage: sudo `dirname $0`/$PROGRAM"
}

usage_and_exit( )
{
  usage
  exit $1
}

version( )
{
  echo "$PROGRAM version $VERSION"
}

read_user_login( )
{
  echo -n "Please enter your PIA username: "
  read LOGIN
  if [ -z $LOGIN ]; then
    error "A login must be provided for the installation to proceed"
  fi
}

verify_running_as_root( )
{
  if [ `/usr/bin/id -u` -ne 0 ]; then
      error_and_usage "$0 must be run as root"
  fi
}

install_python_version( )
{
  if ! dpkg -l python2.7 | grep '^ii' > /dev/null ; then
    echo -n 'Package python2.7 required. Install? (y/n): '
    read install_python
    if [ $install_python = 'y' ]; then
      echo "Installing python2.7.."
      if ! apt-get install python2.7; then
        error "Error installing python2.7 Aborting.."
      fi
    else
      error "Package python2.7 is required for installation. Aborting.."
    fi
  else
    echo "Package python2.7 already installed"
  fi
}

install_open_vpn( )
{
  if ! dpkg -l network-manager-openvpn | grep '^ii' > /dev/null ; then
    echo -n 'Package network-manager-openvpn required. Install? (y/n): '
    read install_openvpn
    if [ $install_openvpn = 'y' ]; then
      echo "Installing network-manager-openvpn.."
      if ! apt-get install network-manager-openvpn; then
        error "Error installing network-manager-openvpn. Aborting.."
      fi
    else
      error "Package network-manager-openvpn is required for installation. Aborting.."
    fi
  else
    echo "Package network-manager-openvpn already installed"
  fi
}

copy_crt( )
{
  echo 'Copying certificate..'
  mkdir -p /etc/openvpn
cat << EOF > /etc/openvpn/ca.crt
-----BEGIN CERTIFICATE-----
MIIFqzCCBJOgAwIBAgIJAKZ7D5Yv87qDMA0GCSqGSIb3DQEBDQUAMIHoMQswCQYD
VQQGEwJVUzELMAkGA1UECBMCQ0ExEzARBgNVBAcTCkxvc0FuZ2VsZXMxIDAeBgNV
BAoTF1ByaXZhdGUgSW50ZXJuZXQgQWNjZXNzMSAwHgYDVQQLExdQcml2YXRlIElu
dGVybmV0IEFjY2VzczEgMB4GA1UEAxMXUHJpdmF0ZSBJbnRlcm5ldCBBY2Nlc3Mx
IDAeBgNVBCkTF1ByaXZhdGUgSW50ZXJuZXQgQWNjZXNzMS8wLQYJKoZIhvcNAQkB
FiBzZWN1cmVAcHJpdmF0ZWludGVybmV0YWNjZXNzLmNvbTAeFw0xNDA0MTcxNzM1
MThaFw0zNDA0MTIxNzM1MThaMIHoMQswCQYDVQQGEwJVUzELMAkGA1UECBMCQ0Ex
EzARBgNVBAcTCkxvc0FuZ2VsZXMxIDAeBgNVBAoTF1ByaXZhdGUgSW50ZXJuZXQg
QWNjZXNzMSAwHgYDVQQLExdQcml2YXRlIEludGVybmV0IEFjY2VzczEgMB4GA1UE
AxMXUHJpdmF0ZSBJbnRlcm5ldCBBY2Nlc3MxIDAeBgNVBCkTF1ByaXZhdGUgSW50
ZXJuZXQgQWNjZXNzMS8wLQYJKoZIhvcNAQkBFiBzZWN1cmVAcHJpdmF0ZWludGVy
bmV0YWNjZXNzLmNvbTCCASIwDQYJKoZIhvcNAQEBBQADggEPADCCAQoCggEBAPXD
L1L9tX6DGf36liA7UBTy5I869z0UVo3lImfOs/GSiFKPtInlesP65577nd7UNzzX
lH/P/CnFPdBWlLp5ze3HRBCc/Avgr5CdMRkEsySL5GHBZsx6w2cayQ2EcRhVTwWp
cdldeNO+pPr9rIgPrtXqT4SWViTQRBeGM8CDxAyTopTsobjSiYZCF9Ta1gunl0G/
8Vfp+SXfYCC+ZzWvP+L1pFhPRqzQQ8k+wMZIovObK1s+nlwPaLyayzw9a8sUnvWB
/5rGPdIYnQWPgoNlLN9HpSmsAcw2z8DXI9pIxbr74cb3/HSfuYGOLkRqrOk6h4RC
OfuWoTrZup1uEOn+fw8CAwEAAaOCAVQwggFQMB0GA1UdDgQWBBQv63nQ/pJAt5tL
y8VJcbHe22ZOsjCCAR8GA1UdIwSCARYwggESgBQv63nQ/pJAt5tLy8VJcbHe22ZO
sqGB7qSB6zCB6DELMAkGA1UEBhMCVVMxCzAJBgNVBAgTAkNBMRMwEQYDVQQHEwpM
b3NBbmdlbGVzMSAwHgYDVQQKExdQcml2YXRlIEludGVybmV0IEFjY2VzczEgMB4G
A1UECxMXUHJpdmF0ZSBJbnRlcm5ldCBBY2Nlc3MxIDAeBgNVBAMTF1ByaXZhdGUg
SW50ZXJuZXQgQWNjZXNzMSAwHgYDVQQpExdQcml2YXRlIEludGVybmV0IEFjY2Vz
czEvMC0GCSqGSIb3DQEJARYgc2VjdXJlQHByaXZhdGVpbnRlcm5ldGFjY2Vzcy5j
b22CCQCmew+WL/O6gzAMBgNVHRMEBTADAQH/MA0GCSqGSIb3DQEBDQUAA4IBAQAn
a5PgrtxfwTumD4+3/SYvwoD66cB8IcK//h1mCzAduU8KgUXocLx7QgJWo9lnZ8xU
ryXvWab2usg4fqk7FPi00bED4f4qVQFVfGfPZIH9QQ7/48bPM9RyfzImZWUCenK3
7pdw4Bvgoys2rHLHbGen7f28knT2j/cbMxd78tQc20TIObGjo8+ISTRclSTRBtyC
GohseKYpTS9himFERpUgNtefvYHbn70mIOzfOJFTVqfrptf9jXa9N8Mpy3ayfodz
1wiqdteqFXkTYoSDctgKMiZ6GdocK9nMroQipIQtpnwd4yBDWIyC6Bvlkrq5TQUt
YDQ8z9v+DMO6iwyIDRiU
-----END CERTIFICATE-----
EOF

}

parse_server_info( )
{
  echo 'Loading servers information..'
  json=`wget -q -O - 'https://privateinternetaccess.com/vpninfo/servers?version=24' | head -1`

  python > $SERVER_INFO <<EOF
payload = '$json'
import json
d = json.loads(payload)
print "\n".join([d[k]['name']+'$SPLIT_TOKEN'+d[k]['dns'] for k in d.keys() if k != 'info'])
EOF
}

write_config_files( )
{
  echo 'Removing previous config files if existing..'
  rm -f /etc/NetworkManager/system-connections/PIA\ -\ *

  echo 'Creating config files..'
  IFS='
'
  while read server_info; do
    name="PIA - `echo $server_info | awk -F: '{print $1}'`"
    dns=`echo $server_info | awk -F: '{print $2}'`
    cat <<EOF > /etc/NetworkManager/system-connections/$name
[connection]
id=$name
uuid=`uuidgen`
type=vpn
autoconnect=false

[vpn]
service-type=org.freedesktop.NetworkManager.openvpn
username=$LOGIN
comp-lzo=yes
remote=$dns
cipher=AES-128-CBC
connection-type=password
password-flags=1
port=1198
ca=/etc/openvpn/ca.crt

[ipv4]
method=auto
EOF
  chmod 600 /etc/NetworkManager/system-connections/$name
  done < $SERVER_INFO
  rm $SERVER_INFO
  IFS='
 	'
}

restart_network_manager( )
{
  echo 'Restarting network manager..'
  /usr/bin/nmcli nm enable false
  /usr/bin/nmcli nm enable true
}

EXITCODE=0
PROGRAM=`basename $0`
VERSION=1.1

while test $# -gt 0
do
  case $1 in
  --usage | --help | -h )
    usage_and_exit 0
    ;;
  --version | -v )
    version
    exit 0
    ;;
  *)
    error_and_usage "Unrecognized option: $1"
    ;;
  esac
  shift
done


verify_running_as_root
install_python_version
install_open_vpn
read_user_login
copy_crt
parse_server_info
write_config_files
restart_network_manager

echo "Install successful!"
exit 0
