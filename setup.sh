export HDMI2USB_UDEV_IGNORE=y
export PLATFORM=pano_logic_g2
#export SKIP_IMAGE=1
#export PLATFORM=arty
export CPU_VARIANT=linux
export BUILD_BUILDROOT=1
export TARGET=net
export TARGET=base
#export FIRMWARE=micropython
export FIRMWARE=linux
export BAUD=961538
export MAKE_LITEX_EXTRA_CMDLINE="--uart-baudrate 961538 -Op uart_connection hdmi --iprange 192.168.123.113,192.168.123.1"
#export MAKE_LITEX_EXTRA_CMDLINE="--uart-baudrate 961538"
export TFTP_SERVER_PORT=69
. ./scripts/enter-env.sh

