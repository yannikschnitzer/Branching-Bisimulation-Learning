//#Safe
//@ ltl invariant positive: AP(c > 5) ==> <> AP(r > 5);

#include <stdio.h> 

extern void __VERIFIER_error() __attribute__ ((__noreturn__));
extern void __VERIFIER_assume() __attribute__ ((__noreturn__));
extern int __VERIFIER_nondet_int() __attribute__ ((__noreturn__));

int c, r, cs;

int main()
{
    c = __VERIFIER_nondet_int();
    r = __VERIFIER_nondet_int();
    cs = __VERIFIER_nondet_int();
    while(1)
    {
        int choice = __VERIFIER_nondet_int();
        if (choice > 1) {
            if (cs <= 0 || c < cs) {
                c = c;
                r = r;
                cs = cs;
            } else {
                c = c - 1;
                r = r + 1;
                cs = cs - 1;
            }
        } else {
            c = c;
            r = r;
            if (cs <= 0 || c < cs) {
                cs = cs;
            } else {
                cs = cs - 1;
            }
        }
    }
}
