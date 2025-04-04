//#Safe
//@ ltl invariant positive: [] <> AP(x >= 1);

#include <stdio.h> 

extern void __VERIFIER_error() __attribute__ ((__noreturn__));
extern void __VERIFIER_assume() __attribute__ ((__noreturn__));
extern int __VERIFIER_nondet_int() __attribute__ ((__noreturn__));

int x;

int main()
{
    x = 10;
    while(1)
    {
        int choice = __VERIFIER_nondet_int();
        if (choice > 1) {
            if (x < 0) {
                x = x;
            } else {
                x = x + 1;
            }
        } else {
            if (x < 0) {
                x = x;
            } else if (x > 5) {
                x = x + 1;
            } else if (x > 2) {
                x = x - 1;
            } else {
                x = x;
            }
        }
    }
}
