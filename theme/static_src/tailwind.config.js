/**
 * This is a minimal config.
 *
 * If you need the full config, get it from here:
 * https://unpkg.com/browse/tailwindcss@latest/stubs/defaultConfig.stub.js
 */

module.exports = {
    content: [
        /**
         * HTML. Paths to Django template files that will contain Tailwind CSS classes.
         */

        /*  Templates within theme app (<tailwind_app_name>/templates), e.g. base.html. */
        '../templates/**/*.html',

        /*
         * Main templates directory of the project (BASE_DIR/templates).
         * Adjust the following line to match your project structure.
         */
        '../../templates/**/*.html',

        /*
         * Templates in other django apps (BASE_DIR/<any_app_name>/templates).
         * Adjust the following line to match your project structure.
         */
        '../../**/templates/**/*.html',

        /**
         * JS: If you use Tailwind CSS in JavaScript, uncomment the following lines and make sure
         * patterns match your project structure.
         */
        /* JS 1: Ignore any JavaScript in node_modules folder. */
        // '!../../**/node_modules',
        /* JS 2: Process all JavaScript files in the project. */
        // '../../**/*.js',

        /**
         * Python: If you use Tailwind CSS classes in Python, uncomment the following line
         * and make sure the pattern below matches your project structure.
         */
        // '../../**/*.py'
    ],
    theme: {
        screens: {
            sm: "340px", 
            md: "540px",
            lg: "768px",
            xl: "1186px",
        },
        extend: {
            keyFrames: {
                shift: {
                    "50%": {
                        transform: "translateY(-1rem)"
                    }
                },
                rotation: {
                    "0%": { transform: "rotate(Odeg)" },
                    "100%": { transform: "rotate(360deg)" }
                },
                scaleUp: {
                    "0%":{ transform: "scale(0.8)" },
                    "50%":{ transform: "scale(1.2)" },
                    "0%":{ transform: "scale(0.8)" }
                }
            },
            animation: {
                movingY: "shift 3s linear infinite",
                rotating: "rotation 15s linear infinite",
                scaling: "scaleUp 5s linear infinite",
            },
        },
        fontFamily: {
            jost: ["Jost", "sans-serif"],
            jua: ["Jua", "serif"],
            barriecito: ["Barriecito", "serif"]
        },
        container: {
            center: true,
            padding: {
                DEFAULT: "12px", 
                md: "32px", 
            }
        }
    },
    plugins: [
        /**
         * '@tailwindcss/forms' is the forms plugin that provides a minimal styling
         * for forms. If you don't like it or have own styling for forms,
         * comment the line below to disable '@tailwindcss/forms'.
         */
        require('@tailwindcss/forms'),
        require('@tailwindcss/typography'),
        require('@tailwindcss/aspect-ratio'),
        require('@tailwindcss/aspect-ratio'),
    ],
}
