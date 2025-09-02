init python:
    renpy.register_shader("2DVfx.simple_gradient", variables="""
    
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

        gl_FragColor = vec4(end, 1.0);""")

    renpy.register_shader("test", variables="""
        uniform vec4 u_radius;
        uniform float u_alias;

        attribute vec2 a_tex_coord;
        varying vec2 v_tex_coord;
        uniform vec2 res0;

        uniform sampler2D tex0;

        """, vertex_300="""

        v_tex_coord = a_tex_coord;

        """, fragment_300="""
        
        vec2 tex_coord_pix = v_tex_coord.xy * res0.xy;
        float distance = roundBorders(tex_coord_pix.xy - (res0.xy / 2.0), res0.xy / 2.0, u_radius);
        float alpha = 1.0 - smoothstep(0.0, u_alias, distance);
        vec4 color = texture2D(tex0, v_tex_coord);
        gl_FragColor = color * alpha;

        """, fragment_functions="""
        
        float roundBorders(vec2 center, vec2 size, vec4 radius) {
            radius = radius.zywx;
            radius.xy = (center.x > 0.0) ? radius.xy : radius.zw;
            radius.x = (center.y > 0.0) ? radius.x : radius.y;
            vec2 q = abs(center) - size + radius.x;
            return min(max(q.x, q.y), 0.0) + length(max(q, 0.0)) - radius.x;}

        """)

    renpy.register_shader("2DVfx.round_mask", variables="""
    
        uniform vec4 u_radius;
        uniform float u_feather;

        uniform sampler2D tex0;
        uniform vec2 res0;

        attribute vec2 a_tex_coord;
        varying vec2 v_tex_coord;

        """, fragment_functions="""
        float roundedBoxSDF(vec2 center, vec2 size, vec4 radius) {
            radius = radius.zywx;
            radius.xy = (center.x > 0.0) ? radius.xy : radius.zw;
            radius.x = (center.y > 0.0) ? radius.x : radius.y;
            vec2 q = abs(center) - size + radius.x;
            return min(max(q.x, q.y), 0.0) + length(max(q, 0.0)) - radius.x;
        }
        """, vertex_300="""

        v_tex_coord = a_tex_coord;

        """, fragment_300="""
        vec2 tex_coord_pix = v_tex_coord.xy * res0.xy;
        float distance = roundedBoxSDF(tex_coord_pix.xy - (res0.xy / 2.0), res0.xy / 2.0, u_radius);
        float alpha = 1.0 - smoothstep(0.0, u_feather, distance);
        gl_FragColor = vec4(0.0, 0.0, 0.0, alpha);""")