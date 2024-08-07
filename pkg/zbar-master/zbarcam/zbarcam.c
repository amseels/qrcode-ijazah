/*------------------------------------------------------------------------
 *  Copyright 2007-2009 (c) Jeff Brown <spadix@users.sourceforge.net>
 *
 *  This file is part of the ZBar Bar Code Reader.
 *
 *  The ZBar Bar Code Reader is free software; you can redistribute it
 *  and/or modify it under the terms of the GNU Lesser Public License as
 *  published by the Free Software Foundation; either version 2.1 of
 *  the License, or (at your option) any later version.
 *
 *  The ZBar Bar Code Reader is distributed in the hope that it will be
 *  useful, but WITHOUT ANY WARRANTY; without even the implied warranty
 *  of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 *  GNU Lesser Public License for more details.
 *
 *  You should have received a copy of the GNU Lesser Public License
 *  along with the ZBar Bar Code Reader; if not, write to the Free
 *  Software Foundation, Inc., 51 Franklin St, Fifth Floor,
 *  Boston, MA  02110-1301  USA
 *
 *  http://sourceforge.net/projects/zbar
 *------------------------------------------------------------------------*/

#include "config.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#ifdef _WIN32
#include <fcntl.h>
#include <io.h>
#include <objbase.h>
#endif
#include <assert.h>

#include <zbar.h>

#ifdef ENABLE_NLS
#include <libintl.h>
#include <locale.h>
#define _(string) gettext(string)
#else
#define _(string) string
#endif

#define N_(string) string

#define BELL "\a"

static const char *note_usage = N_(
    "usage: zbarcam [options] [/dev/video?]\n"
    "\n"
    "scan and decode bar codes from a video stream\n"
    "\n"
    "options:\n"
    "    -h, --help      display this help text\n"
    "    --version       display version information and exit\n"
    "    -q, --quiet     disable beep when symbol is decoded\n"
    "    -v, --verbose   increase debug output level\n"
    "    --verbose=N     set specific debug output level\n"
    "    --xml           use XML output format\n"
    "    --raw           output decoded symbol data without converting charsets\n"
    "    -1, --oneshot   exit after scanning one bar code\n"
    "    --nodisplay     disable video display window\n"
    "    --prescale=<W>x<H>\n"
    "                    request alternate video image size from driver\n"
    "    -S<CONFIG>[=<VALUE>], --set <CONFIG>[=<VALUE>]\n"
    "                    set decoder/scanner <CONFIG> to <VALUE> (or 1)\n"
    /* FIXME overlay level */
    "\n");

#ifdef HAVE_DBUS
static const char *note_usage2 =
    N_("    --nodbus        disable dbus message\n");
#endif

static const char *xml_head =
    "<barcodes xmlns='http://zbar.sourceforge.net/2008/barcode'>"
    "<source device='%s'>\n";
static const char *xml_foot = "</source></barcodes>\n";

static zbar_processor_t *proc;
static int quiet = 0, oneshot = 0;
static enum { DEFAULT, RAW, XML } format = DEFAULT;

static char *xml_buf    = NULL;
static unsigned xml_len = 0;

static int usage(int rc)
{
    FILE *out = (rc) ? stderr : stdout;
    fprintf(out, "%s", _(note_usage));
#ifdef HAVE_DBUS
    fprintf(out, "%s", _(note_usage2));
#endif
    return (rc);
}

static inline int parse_config(const char *cfgstr, int i, int n, char *arg)
{
    if (i >= n || !*cfgstr) {
        fprintf(stderr, "ERROR: need argument for option: %s\n", arg);
        return (1);
    }

    if (zbar_processor_parse_config(proc, cfgstr)) {
        fprintf(stderr, "ERROR: invalid configuration setting: %s\n", cfgstr);
        return (1);
    }
    return (0);
}

static void data_handler(zbar_image_t *img, const void *userdata)
{
    int n                    = 0;
    const zbar_symbol_t *sym = zbar_image_first_symbol(img);
    assert(sym);
    for (; sym; sym = zbar_symbol_next(sym)) {
        zbar_symbol_type_t type;
        if (zbar_symbol_get_count(sym))
            continue;

        type = zbar_symbol_get_type(sym);
        if (type == ZBAR_PARTIAL)
            continue;

        if (!format) {
            printf("%s:", zbar_get_symbol_name(type));
            if (fwrite(zbar_symbol_get_data(sym),
                       zbar_symbol_get_data_length(sym), 1, stdout) != 1)
                continue;
        } else if (format == RAW) {
            if (fwrite(zbar_symbol_get_data(sym),
                       zbar_symbol_get_data_length(sym), 1, stdout) != 1)
                continue;
        } else if (format == XML) {
            if (!n)
                printf("<index num='%u'>\n", zbar_image_get_sequence(img));
            zbar_symbol_xml(sym, &xml_buf, &xml_len);
            if (fwrite(xml_buf, xml_len, 1, stdout) != 1)
                continue;
        }
        n++;

        if (oneshot) {
            if (format != RAW)
                printf("\n");
            break;
        } else
            printf("\n");
    }

    if (format == XML && n)
        printf("</index>\n");
    fflush(stdout);

    if (!quiet && n)
        fprintf(stderr, BELL);
}

int main(int argc, const char *argv[])
{
    const char *video_device;
    int display;
    unsigned long infmt, outfmt;
    int i, active;

#ifdef ENABLE_NLS
    setlocale(LC_ALL, "");
    bindtextdomain(PACKAGE, LOCALEDIR);
    textdomain(PACKAGE);
#endif

#ifdef DIRECTSHOW
    HRESULT res = CoInitializeEx(NULL, COINIT_APARTMENTTHREADED);
    if (FAILED(res)) {
        fprintf(stderr, "ERROR: failed to initialize COM library\n");
        return (1);
    }
#endif

    /* setup zbar library standalone processor,
     * threads will be used if available
     */
    proc = zbar_processor_create(1);
    if (!proc) {
        fprintf(stderr, "ERROR: unable to allocate memory?\n");
        return (1);
    }
    zbar_processor_set_data_handler(proc, data_handler, NULL);

    video_device = "";
#ifdef HAVE_DBUS
    int dbus = 1;
#endif
    display = 1;
    infmt = 0, outfmt = 0;
    for (i = 1; i < argc; i++) {
        if (argv[i][0] != '-')
            video_device = argv[i];
        else if (argv[i][1] != '-') {
            int j;
            for (j = 1; argv[i][j]; j++) {
                if (argv[i][j] == 'S') {
                    if (!argv[i][++j]) {
                        i++;
                        j = 0;
                    }
                    if (parse_config(&argv[i][j], i, argc, "-S"))
                        return (usage(1));
                    break;
                }
                switch (argv[i][j]) {
                case 'h':
                    return (usage(0));
                case 'v':
                    zbar_increase_verbosity();
                    break;
                case 'q':
                    quiet = 1;
                    break;
                case '1':
                    oneshot = 1;
                    break;
                default:
                    fprintf(stderr, "ERROR: unknown bundled config: -%c\n\n",
                            argv[i][j]);
                    return (usage(1));
                }
            }
        } else if (!argv[i][2]) {
            if (i < argc - 1)
                video_device = argv[argc - 1];
            break;
        } else if (!strcmp(argv[i], "--help"))
            return (usage(0));
        else if (!strcmp(argv[i], "--version"))
            return (printf(PACKAGE_VERSION "\n") <= 0);
        else if (!strcmp(argv[i], "--set")) {
            i++;
            if (parse_config(argv[i], i, argc, "--set"))
                return (usage(1));
        } else if (!strncmp(argv[i], "--set=", 6)) {
            if (parse_config(&argv[i][6], i, argc, "--set="))
                return (usage(1));
        } else if (!strcmp(argv[i], "--quiet"))
            quiet = 1;
        else if (!strcmp(argv[i], "--oneshot"))
            oneshot = 1;
        else if (!strcmp(argv[i], "--xml"))
            format = XML;
        else if (!strcmp(argv[i], "--raw"))
            format = RAW;
        else if (!strcmp(argv[i], "--nodbus"))
#ifdef HAVE_DBUS
            dbus = 0;
#else
            ; /* silently ignore the option */
#endif
        else if (!strcmp(argv[i], "--nodisplay"))
            display = 0;
        else if (!strcmp(argv[i], "--verbose"))
            zbar_increase_verbosity();
        else if (!strncmp(argv[i], "--verbose=", 10))
            zbar_set_verbosity(strtol(argv[i] + 10, NULL, 0));
        else if (!strncmp(argv[i], "--prescale=", 11)) {
            char *x    = NULL;
            long int w = strtol(argv[i] + 11, &x, 10);
            long int h = 0;
            if (x && *x == 'x')
                h = strtol(x + 1, NULL, 10);
            if (!w || !h || !x || *x != 'x') {
                fprintf(stderr, "ERROR: invalid prescale: %s\n\n", argv[i]);
                return (usage(1));
            }
            zbar_processor_request_size(proc, w, h);
        } else if (!strncmp(argv[i], "--v4l=", 6)) {
            long int v = strtol(argv[i] + 6, NULL, 0);
            zbar_processor_request_interface(proc, v);
        } else if (!strncmp(argv[i], "--iomode=", 9)) {
            long int v = strtol(argv[i] + 9, NULL, 0);
            zbar_processor_request_iomode(proc, v);
        } else if (!strncmp(argv[i], "--infmt=", 8) && strlen(argv[i]) == 12)
            infmt = (argv[i][8] | (argv[i][9] << 8) | (argv[i][10] << 16) |
                     (argv[i][11] << 24));
        else if (!strncmp(argv[i], "--outfmt=", 9) && strlen(argv[i]) == 13)
            outfmt = (argv[i][9] | (argv[i][10] << 8) | (argv[i][11] << 16) |
                      (argv[i][12] << 24));
        else {
            fprintf(stderr, "ERROR: unknown option argument: %s\n\n", argv[i]);
            return (usage(1));
        }
    }

    if (infmt || outfmt)
        zbar_processor_force_format(proc, infmt, outfmt);

#ifdef HAVE_DBUS
    zbar_processor_request_dbus(proc, dbus);
#endif

    /* open video device, open window */
    if (zbar_processor_init(proc, video_device, display) ||
        /* show window */
        (display && zbar_processor_set_visible(proc, 1)))
        return (zbar_processor_error_spew(proc, 0));

#ifdef _WIN32
    if (format == XML || format == RAW) {
        fflush(stdout);
        if (_setmode(_fileno(stdout), _O_BINARY) == -1) {
            fprintf(stderr, "ERROR: failed to set stdout mode: %i\n", errno);
            return (1);
        }
    }
#endif

    if (format == XML) {
        printf(xml_head, video_device);
        fflush(stdout);
    }

    /* start video */
    active = 1;
    if (zbar_processor_set_active(proc, active))
        return (zbar_processor_error_spew(proc, 0));

    if (oneshot) {
        if (zbar_process_one(proc, -1) < 0)
            if (zbar_processor_get_error_code(proc) != ZBAR_ERR_CLOSED)
                return zbar_processor_error_spew(proc, 0);
    } else {
        /* let the callback handle data */
        int rc;
        while ((rc = zbar_processor_user_wait(proc, -1)) >= 0) {
            if (rc == 'q' || rc == 'Q')
                break;
            // HACK: controls are known on V4L2 by ID, not by name. This is also
            // not compatible with other platforms
            if (rc == 'b' || rc == 'B') {
                int value;
                zbar_processor_get_control(proc, "Brightness", &value);
                zbar_processor_set_control(proc, "Brightness", ++value);
            }
            if (rc == 'n' || rc == 'N') {
                int value;
                zbar_processor_get_control(proc, "Brightness", &value);
                zbar_processor_set_control(proc, "Brightness", --value);
            }
            if (rc == ' ') {
                active = !active;
                if (zbar_processor_set_active(proc, active))
                    return (zbar_processor_error_spew(proc, 0));
            }
        }

        /* report any errors that aren't "window closed" */
        if (rc && rc != 'q' && rc != 'Q' &&
            zbar_processor_get_error_code(proc) != ZBAR_ERR_CLOSED)
            return (zbar_processor_error_spew(proc, 0));
    }

    /* free resources (leak check) */
    zbar_processor_destroy(proc);

    if (format == XML) {
        printf("%s", xml_foot);
        fflush(stdout);
    }
    return (0);
}
