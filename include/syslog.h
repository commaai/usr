/*
 * Copyright (C) 2008 The Android Open Source Project
 * All rights reserved.
 *
 * Redistribution and use in source and binary forms, with or without
 * modification, are permitted provided that the following conditions
 * are met:
 *  * Redistributions of source code must retain the above copyright
 *    notice, this list of conditions and the following disclaimer.
 *  * Redistributions in binary form must reproduce the above copyright
 *    notice, this list of conditions and the following disclaimer in
 *    the documentation and/or other materials provided with the
 *    distribution.
 *
 * THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
 * "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
 * LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
 * FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
 * COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
 * INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
 * BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS
 * OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED
 * AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
 * OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT
 * OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF
 * SUCH DAMAGE.
 */

#ifndef _SYSLOG_H
#define _SYSLOG_H

#include <stdio.h>
#include <sys/cdefs.h>
#include <stdarg.h>
#include <android/log.h> /* for __android_log_vprint() */
#include <unistd.h> /* for getpid() */

__BEGIN_DECLS

/* Priorities are translated to Android log priorities as shown. */
#define LOG_EMERG   0 /* ERROR */
#define LOG_ALERT   1 /* ERROR */
#define LOG_CRIT    2 /* ERROR */
#define LOG_ERR     3 /* ERROR */
#define LOG_WARNING 4 /* WARN */
#define LOG_NOTICE  5 /* INFO */
#define LOG_INFO    6 /* INFO */
#define LOG_DEBUG   7 /* DEBUG */

#define LOG_PRIMASK 7
#define LOG_PRI(x) ((x) & LOG_PRIMASK)
#define LOG_MAKEPRI(fac, pri) ((fac) | (pri))

/* Facilities are currently ignored on Android. */
#define LOG_KERN     (0<<3)
#define LOG_USER     (1<<3)
#define LOG_MAIL     (2<<3)
#define LOG_DAEMON   (3<<3)
#define LOG_AUTH     (4<<3)
#define LOG_SYSLOG   (5<<3)
#define LOG_LPR      (6<<3)
#define LOG_NEWS     (7<<3)
#define LOG_UUCP     (8<<3)
#define LOG_CRON     (9<<3)
#define LOG_AUTHPRIV (10<<3)
#define LOG_FTP      (11<<3)
#define LOG_LOCAL0   (16<<3)
#define LOG_LOCAL1   (17<<3)
#define LOG_LOCAL2   (18<<3)
#define LOG_LOCAL3   (19<<3)
#define LOG_LOCAL4   (20<<3)
#define LOG_LOCAL5   (21<<3)
#define LOG_LOCAL6   (22<<3)
#define LOG_LOCAL7   (23<<3)

#define LOG_NFACILITIES 24
#define LOG_FACMASK 0x3f8
#define LOG_FAC(x) (((x) >> 3) & (LOG_FACMASK >> 3))

#define LOG_MASK(pri) (1 << (pri))
#define LOG_UPTO(pri) ((1 << ((pri)+1)) - 1)

/* openlog(3) flags are currently ignored on Android. */
#define LOG_PID    0x01
#define LOG_CONS   0x02
#define LOG_ODELAY 0x04
#define LOG_NDELAY 0x08
#define LOG_NOWAIT 0x10
#define LOG_PERROR 0x20

void closelog(void);
void openlog(const char* __prefix, int __option, int __facility);
int setlogmask(int __mask);
void syslog(int __priority, const char* __fmt, ...) __printflike(2, 3);
void vsyslog(int __priority, const char* __fmt, va_list __args) __printflike(2, 0);

extern /*const*/ char* __progname;
static __inline__ void android_polyfill_openlog(const char* a, int b, int c) {
	(void) a;
	(void) b;
	(void) c;
}
static __inline__ void android_polyfill_closelog() {}

static __inline__ void android_polyfill_vsyslog(int syslog_priority, char const* format, va_list ap)
{
	android_LogPriority a = ANDROID_LOG_ERROR;
	switch (syslog_priority) {
		case LOG_WARNING: a = ANDROID_LOG_WARN; break;
		case LOG_NOTICE	: a = ANDROID_LOG_INFO; break;
		case LOG_INFO: a = ANDROID_LOG_INFO; break;
		case LOG_DEBUG: a = ANDROID_LOG_DEBUG; break;
	}
	char* syslog_text;
	if (vasprintf(&syslog_text, format, ap) == -1) {
       	__android_log_vprint(a, "syslog", format, ap);
		return;
	}
	__android_log_print(a, "syslog", "%s - %s", __progname, syslog_text);
	free(syslog_text);
}

static __inline__ void android_polyfill_syslog(int priority, const char* format, ...)
{
	va_list myargs;
	va_start(myargs, format);
	android_polyfill_vsyslog(priority, format, myargs);
	va_end(myargs);
}

static __inline__ void android_polyfill_syslog_r(int syslog_priority, void* d, const char* format, ...)
{
	(void) d;
	va_list myargs;
	va_start(myargs, format);
	android_polyfill_vsyslog(syslog_priority, format, myargs);
	va_end(myargs);
}

static __inline__ void android_polyfill_vsyslog_r(int syslog_priority, void* d, const char* fmt, va_list ap)
{
	(void) d;
	android_polyfill_vsyslog(syslog_priority, fmt, ap);
}

#define openlog android_polyfill_openlog
#define closelog android_polyfill_closelog

#define syslog android_polyfill_syslog
#define syslog_r android_polyfill_syslog_r

#define vsyslog android_polyfill_vsyslog
#define vsyslog_r android_polyfill_vsyslog_r

__END_DECLS

#endif /* _SYSLOG_H */
