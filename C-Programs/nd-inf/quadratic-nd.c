
#include <stdio.h> 

extern void __VERIFIER_error() __attribute__ ((__noreturn__));
extern void __VERIFIER_assume() __attribute__ ((__noreturn__));
extern int __VERIFIER_nondet_int() __attribute__ ((__noreturn__));

int x;

int main()
{
    x = __VERIFIER_nondet_int();
    while(1)
    {
        int terminated = x < 0 || x > 1000;
        if (!terminated) {

            int a = __VERIFIER_nondet_int();
            if (a > 0) {
                x = x + 1;
            } else {
                x = x * x;
            }
        }
        else {
            x = x;
        }
    }
}
