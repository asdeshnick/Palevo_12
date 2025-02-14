#include <pcap.h>
#include <iostream>

void packet_handler(u_char *args, const struct pcap_pkthdr *header, const u_char *packet) {
    std::cout << "Packet captured: length=" << header->len << std::endl;
}

int main() {
    char errbuf[PCAP_ERRBUF_SIZE];
    pcap_t *handle = pcap_open_live("eth0", BUFSIZ, 1, 1000, errbuf);
    if (handle == nullptr) {
        std::cerr << "Error opening device: " << errbuf << std::endl;
        return 1;
    }

    pcap_loop(handle, -1, packet_handler, nullptr);

    pcap_close(handle);
    return 0;
}




