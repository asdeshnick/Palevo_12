#include <openssl/rsa.h>
#include <openssl/bio.h>
#include <openssl/pem.h>
#include <iostream>

int main() {
    RSA *keypair = RSA_generate_key(2048, RSA_F4, NULL, NULL);
    if (!keypair) {
        std::cerr << "Failed to generate key pair" << std::endl;
        return 1;
    }

    BIO *bio_pub = BIO_new(BIO_s_mem());
    BIO *bio_priv = BIO_new(BIO_s_mem());

    PEM_write_bio_RSAPublicKey(bio_pub, keypair);
    PEM_write_bio_RSAPrivateKey(bio_priv, keypair, NULL, NULL, 0, NULL, NULL);

    char *pub_key_str = NULL;
    int pub_len = BIO_get_mem_data(bio_pub, &pub_key_str);
    std::cout << "Public Key: " << std::string(pub_key_str, pub_len) << std::endl;

    char *priv_key_str = NULL;
    int priv_len = BIO_get_mem_data(bio_priv, &priv_key_str);
    std::cout << "Private Key: " << std::string(priv_key_str, priv_len) << std::endl;

    RSA_free(keypair);
    BIO_free_all(bio_pub);
    BIO_free_all(bio_priv);

    return 0;
}