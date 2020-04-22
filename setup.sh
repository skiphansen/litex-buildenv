export HDMI2USB_UDEV_IGNORE=y
export PLATFORM=pano_logic_g2
#export CPU_VARIANT=linux
#export BUILD_BUILDROOT=1
export TARGET=net
#export TARGET=base
#export FIRMWARE=linux
export BAUD=961538
export MAKE_LITEX_EXTRA_CMDLINE="--uart-baudrate 961538 -Op uart_connection hdmi"
#export MAKE_LITEX_EXTRA_CMDLINE="--uart-baudrate 961538"
. ./scripts/enter-env.sh

