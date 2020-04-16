# Support for the Pano Logic Zero Client G2
from migen import *

from litex.soc.integration.soc_sdram import *
from litex.soc.integration.builder import *
from litex.soc.interconnect import wishbone

from litedram.modules import MT47H32M16
from litedram.phy import s6ddrphy
from litedram.core import ControllerSettings

from gateware import cas
from gateware import info
from gateware import spi_flash

from .crg import _CRG

from targets.utils import dict_set_max

class BaseSoC(SoCSDRAM):
    mem_map = {**SoCSDRAM.mem_map, **{
        'spiflash': 0x20000000,
        'emulator_ram': 0x50000000,
    }}

    def __init__(self, platform, **kwargs):
        dict_set_max(kwargs, 'integrated_rom_size', 0x8000)
        dict_set_max(kwargs, 'integrated_sram_size', 0x8000)

        sys_clk_freq = int(50e6)
        # SoCSDRAM ---------------------------------------------------------------------------------
        SoCSDRAM.__init__(self, platform, clk_freq=sys_clk_freq, **kwargs)

        # CRG --------------------------------------------------------------------------------------
        self.submodules.crg = _CRG(platform, sys_clk_freq)
        self.platform.add_period_constraint(self.crg.cd_sys.clk, 1e9/sys_clk_freq)

        # DDR2 SDRAM -------------------------------------------------------------------------------
        if True:
            sdram_module = MT47H32M16(sys_clk_freq, "1:2")
            self.submodules.ddrphy = s6ddrphy.S6HalfRateDDRPHY(
                platform.request("ddram_b"),
                memtype      = sdram_module.memtype,
                rd_bitslip   = 0,
                wr_bitslip   = 4,
                dqs_ddr_alignment="C0")
            self.add_csr("ddrphy")
            controller_settings = ControllerSettings(
                with_bandwidth=True)
            self.register_sdram(
                self.ddrphy,
                geom_settings   = sdram_module.geom_settings,
                timing_settings = sdram_module.timing_settings,
                controller_settings=controller_settings)
            self.comb += [
                self.ddrphy.clk4x_wr_strb.eq(self.crg.clk4x_wr_strb),
                self.ddrphy.clk4x_rd_strb.eq(self.crg.clk4x_rd_strb),
            ]

        # Basic peripherals ------------------------------------------------------------------------
        # info module
        self.submodules.info = info.Info(platform, self.__class__.__name__)
        self.add_csr("info")
        # control and status module
        self.submodules.cas = cas.ControlAndStatus(platform, sys_clk_freq)
        self.add_csr("cas")

        # Add debug interface if the CPU has one ---------------------------------------------------
        if hasattr(self.cpu, "debug_bus"):
            self.register_mem(
                name="vexriscv_debug",
                address=0xf00f0000,
                interface=self.cpu.debug_bus,
                size=0x100)

        # ??????
        gmii_rst_n = platform.request("gmii_rst_n")
        self.comb += [
            gmii_rst_n.eq(1)
        ]


        # Support for soft-emulation for full Linux support ----------------------------------------
        if self.cpu_type == "vexriscv" and self.cpu_variant == "linux":
            size = 0x4000
            self.submodules.emulator_ram = wishbone.SRAM(size)
            self.register_mem("emulator_ram", self.mem_map["emulator_ram"], self.emulator_ram.bus, size)


SoC = BaseSoC
