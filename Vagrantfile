Vagrant.configure("2") do |config|
  pwd = File.expand_path(".", __dir__)

  config.vagrant.plugins = "vagrant-libvirt"

  config.vm.provider :libvirt do |libvirt|
    libvirt.qemu_use_session = true

    libvirt.default_prefix = "homelab-k8s-dev-"

    libvirt.boot "hd"
    libvirt.boot "cdrom"
    libvirt.mgmt_attach = true

    libvirt.cpu_mode = 'host-passthrough'

    libvirt.loader = "/run/libvirt/nix-ovmf/edk2-x86_64-code.fd"
    libvirt.nvram = pwd + "/dev/vms/nvram/edk2-i386-vars.fd"
    libvirt.tpm_type = "emulator"
    libvirt.tpm_version = "2.0"
  end

  config.vm.define "sun" do |vm|
    vm.vm.provider :libvirt do |domain|
      domain.cpus = 2
      domain.memory = 4096

      domain.serial :type => "file", :source => { :path => pwd + "/dev/vms/sun/serial.log" }
      domain.storage :file, :device => :cdrom, :path => pwd + "/dev/vms/sun/metal-amd64.iso"
      domain.storage :file, :size => "200G", :type => "qcow2"
    end
  end
end
