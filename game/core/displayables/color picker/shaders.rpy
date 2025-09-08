init python:
    HLS_FUNC = """
        vec3 hls2rgb(float h, float s, float l) {
            float hp = h / 60.0;
            float c = (1.0 - abs(2.0 * l - 1.0)) * s;
            float m = l - c/2.0;
            float x = c * (1.0 - abs(mod(hp, 2.0) - 1.0));

            vec3 rgb;

            if (hp <= 1.0) {
                rgb = vec3(c, x, 0.0);
            
            } else if (hp <= 2.0) {
                rgb = vec3(x, c, 0.0);
            
            } else if (hp <= 3.0) {
                rgb = vec3(0.0, c, x);
            
            } else if (hp <= 4.0) {
                rgb = vec3(0.0, x, c);

            } else if (hp <= 5.0) {
                rgb = vec3(x, 0.0, c);

            } else {
                rgb = vec3(c, 0.0, x);
                
            }

            return rgb + m;
        }
    """

    renpy.register_shader("2DVfx.square_gradient", variables="""
    
        uniform vec4 u_bottom_right;
        uniform vec4 u_bottom_left;
        uniform vec4 u_top_right;
        uniform vec4 u_top_left;

        attribute vec4 a_tex_coord;
        varying vec4 v_tex_coord;

        """, vertex_300="""

        v_tex_coord = a_tex_coord;

        """, fragment_300="""
        vec2 uv = v_tex_coord.xy;

        vec3 back = mix(u_top_left.rgb, u_top_right.rgb, uv.x);
        vec3 front = mix(u_bottom_left.rgb, u_bottom_right.rgb, uv.x);
        vec3 end = mix(back, front, uv.y);

        gl_FragColor = vec4(end, 1.0);
        """)

    renpy.register_shader("2DVfx.spectrum_gradient", variables="""

        uniform float u_angle;
        attribute vec2 a_tex_coord;
        varying vec2 v_tex_coord;

        """, fragment_functions=HLS_FUNC, vertex_300="""

        v_tex_coord = a_tex_coord.xy;

        """, fragment_300="""
        float t;

        if (u_angle != 0.0) {
            t = v_tex_coord.y;
        
        } else {
            t = v_tex_coord.x;}

        float hue = t * 360.0;

        float sat = 1.0;
        float light = 0.5;

        vec3 color = hls2rgb(hue, sat, light);

        gl_FragColor = vec4(color, 1.0);""")

    renpy.register_shader("2DVfx.radial_hsl_gradient", variables="""

        uniform float u_alias_factor;
        uniform float u_thickness;
        uniform float u_radius;
        uniform vec2 u_center;

        attribute vec4 a_position;
        varying vec2 v_position;

        """, vertex_300="""
        
        v_position = a_position.xy;

        """, fragment_functions=HLS_FUNC, fragment_300="""

        float sat = 1.0;
        float light = 0.5;
        float pi = 3.14159265;

        vec2 pos = v_position - vec2(u_radius, u_radius);
        float dist = distance(pos, u_center);

        float color_offset = radians(135.0);
        float color_angle = atan(pos.y, pos.x);
        color_angle = mod(color_angle + color_offset, 2.0 * pi);
        float hue = mod((color_angle / (2.0 * pi)) + 1.0, 1.0) * 360.0;

        vec3 color = hls2rgb(hue, sat, light);

        float inner_radius = u_radius - u_thickness;
        float alpha_outer = smoothstep(u_radius, u_radius - u_alias_factor, dist);
        float alpha_inner = 0.0;

        if (u_thickness < u_radius) alpha_inner = smoothstep(inner_radius + u_alias_factor, inner_radius, dist);

        if (dist <= u_radius && dist >= inner_radius) {
            float alpha = alpha_outer * (1.0 - alpha_inner) + alpha_inner * (1.0 - alpha_outer);
            gl_FragColor = mix(vec4(0.0), vec4(color, 1.0), alpha);
            
        } else {
            gl_FragColor = vec4(0.0);}""")