#include<stdio.h>
#include<ctype.h>
#define MAX 100
void conToupper(char *aPtr);
int main (void){
int port_no; //changed
    char exit[MAX];
    char a[MAX] = "exit server";


    printf("If you'd like to end, input 'exit server':");
    scanf("%s", &exit);

    for(int i=0; i<MAX; i++){
        if (exit[i] == a[i]){
            conToupper(a);
            printf("%s\n",a);
        break;
        }
    }
}

void conToupper(char *aPtr){
        while(*aPtr != '\0'){
            *aPtr = toupper(*aPtr);
            ++aPtr;
        }
    }
