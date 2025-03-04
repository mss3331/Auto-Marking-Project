

#include<stdio.h>
#include<sys/types.h>
#include<sys/socket.h>
#include<sys/un.h>
#include<unistd.h>
#include<stdlib.h>
#include<netinet/in.h>
#include<arpa/inet.h>
#include<signal.h>

int main(int argc,char *argv[])
{
    int server_sockfd,client_sockfd;
    int server_len,client_len;

    struct sockaddr_in server_address;
    struct sockaddr_in client_address; unlink("server_sockfd");
    server_sockfd = socket(AF_INET,SOCK_STREAM,0);

    server_address.sin_family = AF_INET;
    server_address.sin_addr.s_addr = inet_addr("127.0.0.1");
    server_address.sin_port = htons(9734);
    server_len = sizeof(server_address);
    bind(server_sockfd,(struct sockaddr *)&server_address,server_len);
    listen(server_sockfd,5);
    signal(SIGCHLD,SIG_IGN);
    while(1)
    {
        char ch;
        printf("server waiting!\n");
        client_len = sizeof(client_address);
        client_sockfd = accept(server_sockfd,(struct sockaddr *)&client_address,&client_len);
        if(fork() == 0)
        {
        read(client_sockfd,&ch,1);
        sleep(5);
        ch++;
        write(client_sockfd,&ch,1);
        close(client_sockfd);
        exit(0);
        }
        else
            close(client_sockfd);
    }
    // return 0;
}
