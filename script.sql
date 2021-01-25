INSERT INTO netoli.jornada_tipo_jornada VALUES("A","Alumnos Consejeros");
INSERT INTO netoli.jornada_tipo_jornada VALUES("B","Barra de Café");
INSERT INTO netoli.jornada_tipo_jornada VALUES("C","Cafetería");
INSERT INTO netoli.jornada_tipo_jornada VALUES("D","Director");
INSERT INTO netoli.jornada_tipo_jornada VALUES("O","Otros");
INSERT INTO netoli.jornada_tipo_jornada VALUES("P","Papelería");
INSERT INTO netoli.jornada_tipo_jornada VALUES("S","Subdirector");
SELECT * FROM netoli.jornada_tipo_jornada;

INSERT INTO netoli.votante_tipo_votante VALUES(0,"Alumno");
INSERT INTO netoli.votante_tipo_votante VALUES(1,"Docente");
INSERT INTO netoli.votante_tipo_votante VALUES(2,"PAAE");
SELECT * FROM netoli.votante_tipo_votante;

INSERT INTO netoli.administrador_administrador VALUES("administrador@administrador.ipn.mx","password",1);
SELECT * FROM netoli.administrador_administrador;