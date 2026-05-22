/*============================================================================
* Super-Simple Tasker (SST/C) Example
*
* Copyright (C) 2006-2023 Quantum Leaps, <state-machine.com>.
*
* SPDX-License-Identifier: MIT
*
* Permission is hereby granted, free of charge, to any person obtaining a
* copy of this software and associated documentation files (the "Software"),
* to deal in the Software without restriction, including without limitation
* the rights to use, copy, modify, merge, publish, distribute, sublicense,
* and/or sell copies of the Software, and to permit persons to whom the
* Software is furnished to do so, subject to the following conditions:
*
* The above copyright notice and this permission notice shall be included in
* all copies or substantial portions of the Software.
*
* THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
* IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
* FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
* THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
* LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
* FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
* DEALINGS IN THE SOFTWARE.
============================================================================*/
#include "sst.h"           /* SST framework */
#include "bsp.h"           /* Board Support Package interface */
#include "blinky.h"        /* application shared interface */

/*..........................................................................*/
int main() {
    SST_init(); /* initialize the SST kernel */
    BSP_init(); /* initialize the Board Support Package */

    /* instantiate and start all SST tasks... */
    Blinky_instantiate();
    static SST_Evt const *blinkyQSto[10]; /* Event queue storage */
    SST_Task_start(
        AO_Blinky,     /* AO pointer to start */
        1U,            /* SST-priority */
        blinkyQSto,    /* storage for the AO's queue */
        ARRAY_NELEM(blinkyQSto),   /* queue length */
        (void *)0);    /* initialization event (not used) */

    return SST_Task_run(); /* run the SST tasks */
    /* NOTE; in embedded systems SST_Task_run() should not return */
}

/* 링킹 에러를 해결하기 위한 가짜(Stub) 함수 정의 - bsp.h의 선언에 맞춤 */
void SST_onStart(void) {}
void SST_onIdle(void) {}
void DBC_fault_handler(char const * const file, int line) { (void)file; (void)line; while(1); }
void BSP_init(void) {}
void BSP_ledOn(void) {}    /* 매개변수 제거 */
void BSP_ledOff(void) {}   /* 매개변수 제거 */

/* 시스템 관련 변수 및 함수 */
unsigned int SystemCoreClock = 16000000;
void SystemCoreClockUpdate(void) {}