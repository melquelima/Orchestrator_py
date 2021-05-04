$(document).ready(function(){
    $('#date').mask('00/00/0000');
    
});

var app = angular.module('myApp', [], function($interpolateProvider) {
    $interpolateProvider.startSymbol('[{');
    $interpolateProvider.endSymbol('}]');
});

app.factory('svc', function () {
    var msg="original...";
    return {
        setMessage: function(x) {
            alert(x)
        },
        getMessage: function() {
            return msg;
        }
    };
});

app.service('api_service', ['$q','$http',function($q,$http){  

    Temas = function(method,data){
        parameters = {url: "/api/temas",method: method,data:data}
        return $http(parameters).then(success,error)
    };
    Maquinas = function(method,data){
        parameters = {url: "/api/maquinas",method: method,data:data}
        return $http(parameters).then(success,error)
    };
    Locadores = function(method,data){
        parameters = {url: "/api/locador",method: method,data:data}
        return $http(parameters).then(success,error)
    };
    Usuarios = function(method,data){
        parameters = {url: "/api/usuarios",method: method,data:data}
        return $http(parameters).then(success,error)
    };

    this.getTemas = () => Temas("GET")
    this.postTemas = data => Temas("POST",data)
    this.getMaquina = () => Maquinas("GET")
    this.putMaquina = data => Maquinas("PUT",data)
    this.postMaquina = data => Maquinas("POST",data)
    this.getLocadores = () => Locadores("GET")
    this.getLocadores2 = () => Locadores("FILTER")
    this.postLocadores = data => Locadores("POST",data)
    this.putLocadores = data => Locadores("PUT",data)
    this.getUsuarios2 = () => Usuarios("GET")
    this.postUsuarios = data => Usuarios("POST",data)
    this.putUsuarios = data => Usuarios("PUT",data)
    this.creditUsuarios = data => Usuarios("CREDIT",data)
    
    this.gerarToken = function(data){
        parameters = {url: "/api/updateToken",method: "POST",data:data}
        return $http(parameters).then(success,error)
    };  

    this.salvarStatus = function(data){
        parameters = {url: "/api/maquinas/status",method: "POST",data:data}
        return $http(parameters).then(success,error)
    }
    this.getLogs = function(){
        parameters = {url: "/api/logMaquinas",method: "GET"}
        return $http(parameters).then(success,error)
    }
    this.getDocs = function(){
        parameters = {url: "/api/documentos",method: "GET"}
        return $http(parameters).then(success,error)
    }
    this.getLogsFiltered = function(data){
        parameters = {url: "/api/logMaquinasFilter",method: "POST",data:data}
        return $http(parameters).then(success,error)
    }
    this.getUsuarios = function(obj){
        id_locador = obj.id_locador==null?(obj.id_user==null?"":"/*"): "/" + obj.id_locador
        id_user = obj.id_user==null?"": "/" + obj.id_user

        if (obj.id_user + obj.id_locador == "" && !obj.admin){
            id_locador = "/" + obj.id_usuarioAtual
        }

        parameters = {url: "/api/usuarios"+id_locador + id_user,method: "GET"}
        return $http(parameters).then(success,error)
    }

    this.getLocadores2 = function(obj){
        id_locador = obj.id_locador==null?"": "/" + obj.id_locador
        parameters = {url: "/api/locador"+id_locador,method: "FILTER"}
        return $http(parameters).then(success,error)
    }



    this.getMaquinaId = function(obj){
        id_locador = obj.id_locador==null?(obj.id_maquina==null?"":"/*"): "/" + obj.id_locador
        id_maquina = obj.id_maquina==null?"": "/" + obj.id_maquina

        if (obj.id_maquina + obj.id_locador == "" && !obj.admin){
            id_locador = "/" + obj.id_usuarioAtual
        }

        parameters = {url: "/api/maquinas"+id_locador + id_maquina,method: "GET"}
        return $http(parameters).then(success,error)
    }

    
    success = (response)=> response.data
    error = (response)=> {toastr.error(response.data);return $q.reject(response.data)}

}]);

app.service('tema_svc', ['api_service',function(api_service){  

    this.cadastraTema = novoTema=>{
        
        if(novoTema == undefined){
            return toastr.warning('o campo nao pode estar vazio');
        }
        
        if(novoTema.trim() == ''){
            return toastr.warning('o campo nao pode estar vazio');
        }

        data = {tema:novoTema}
        return api_service.postTemas(data)
    }

}]);

app.service('locador_svc', ['api_service',function(api_service){  

    this.validaLocador = locador => {
        obj = JSON.parse(JSON.stringify(locador));
        
        notEmpty = ["nome","telefone","numero_documento","email","local","endereco","user_name","senha","senha2"]
        for(var i=0;i<notEmpty.length;i++){
            if(obj[notEmpty[i]] == null || obj[notEmpty[i]].trim() == ''){
                toastr.warning('o campo ' + notEmpty[i] +  ' não pode estar vazio');
                return false
            }
        }
        if(obj.id_doc_type == null){
            toastr.warning('o campo tipo_do_documento não pode estar vazio');
            return false
        }
        obj.id_doc_type = obj.id_doc_type.id

        if(obj.senha.trim() != obj.senha2.trim()){
            toastr.warning('as senhas não conferem');
            return false
        }
        return true
    }

    this.cadastraLocador = locador => {
        if (this.validaLocador(locador)){
            return api_service.postLocadores(obj)
        }
    }
    this.salvaLocador = locador => {
        if (this.validaLocador(locador)){
            return api_service.putLocadores(obj)
        }
    }

}]);

app.service('api_service2', ['$q','$http',function($q,$http){  

    Bots = function(method,data){
        parameters = {url: "/api/tbl_bots",method: method,data:data}
        return $http(parameters).then(success,error)
    };
    Env = function(method,data){
        parameters = {url: "/api/tbl_env",method: method,data:data}
        return $http(parameters).then(success,error)
    };
    Notepads = function(method,data){
        parameters = {url: "/api/tbl_notepads",method: method,data:data}
        return $http(parameters).then(success,error)
    };
    Token = function(method,data){
        parameters = {url: "/api/updateToken",method: method,data:data}
        return $http(parameters).then(success,error)
    };

    this.getBots = () => Bots("GET")
    this.getEnvs = () => Env("GET")
    this.updateBot = data => Bots("PUT",data)
    this.addBot = data => Bots("POST",data)
    this.updateToken = (data) => Token("POST",data)
    this.getNotepads = () => Notepads("GET")
    this.newNotepad = (data) => Notepads("POST",data)
    
    success = (response)=> response.data
    error = (response)=> {toastr.error(response.data);return $q.reject(response.data)}

}]);


INCLUDES = ['$scope','$filter','$http','$sce','api_service2']

app.controller('TodasCtrl', INCLUDES.concat(['tema_svc',function (sc, $filter,$http,$sce,api_service,tema_svc){
    sc.lista = []//FROMBACKEND.lista
    sc.Selected = {ativa:false}
    sc.temas = []
    sc.envs = []
    sc.loading = true
    sc.loadingSalvar = false
    sc.tokenLoading=false
    sc.token = "sdfsdfsdfsd"
    

    refresh = ()=>{
        sc.Selected ={}
        sc.loading = true
        api_service.getBots().then((r)=>{
            sc.lista = r
            sc.loading = false;
        }).catch(()=>sc.loading = false)
    }

    sc.select = (item)=>{
        print(item)
        sc.token = ""
        sc.Selected = item
        sc.Selected.Env = sc.envs.filter((i)=>{if(i.id == item.Env.id)return i})[0]
        $("#modal-editar").modal("show")
    }

    sc.AlterarMaquina = ()=>{
        obj = JSON.parse(JSON.stringify(sc.Selected));
        if(obj.Env.id == null){
            toastr.warning('o campo "Ambiente" não pode estar vazio');
            return
        }
        if(obj.botName == null | obj.botName.trim() == ""){
            toastr.warning('o campo "Nome" não pode estar vazio');
            return
        }

        if(obj.descricao == null){
            obj.descricao = ""
        }
        if(obj.idChat == null || obj.idChat == ""){
            obj.idChat = 0
        }

        obj.id_Env = obj.Env.id
        sc.loadingSalvar = true
        api_service.updateBot(obj).then((r)=>{
            sc.Selected ={}
            refresh()
            sc.loadingSalvar = false
            $("#modal-editar").modal("hide")
            toastr.success('Dados salvos com sucesso!')
        }).catch(()=>sc.loadingSalvar = false)
    }

    sc.updateToken = ()=>{
        sc.tokenLoading=true

        api_service.updateToken({id:1}).then((r)=>{
            sc.token = r
            sc.tokenLoading=false
        }).catch((r)=>sc.tokenLoading=false)
    }
    
    if (FROMBACKEND.admin){
        sc.FROMBACKEND = FROMBACKEND
        api_service.getEnvs().then((r)=>sc.envs = r)
    }
    refresh();

}]));

app.controller('NovoBotCtrl', INCLUDES.concat(['tema_svc',function (sc, $filter,$http,$sce,api_service,tema_svc){
    sc.temas = []
    sc.novoBot = {botName:null,id_Env:null,descricao:null,idChat:null,pingTimeout:null,pingMinutesTimeout:5}
    sc.envs = []
    sc.loading = true
    sc.loadingButton = false

    api_service.getEnvs().then((r)=>{sc.envs = r;sc.loading = false})


    sc.cadastraBot = (novaMaquina)=>{
        obj = JSON.parse(JSON.stringify(novaMaquina));

        if(obj.id_Env == null){
            toastr.warning('o campo "Ambiente" não pode estar vazio');
            return
        }
        if(obj.botName == null || obj.botName.trim() == ""){
            toastr.warning('o campo "Nome" não pode estar vazio');
            return
        }

        if(obj.descricao == null){
            obj.descricao = ""
        }
        if(obj.idChat == null){
            obj.idChat = 0
        }
        if(obj.pingMinutesTimeout == null || obj.pingMinutesTimeout == 0){
            toastr.warning('Insira o timeout desejado!');
            return
        }

        obj.id_Env = obj.id_Env.id
        print(obj)
        sc.loadingButton = true
        api_service.addBot(obj).then((r)=>{
            sc.loadingButton = false
            toastr.success('Bot Cadastrado com sucesso!');
            sc.novoBot = {pingMinutesTimeout:5}
        }).catch(()=>sc.loadingButton = false)
    }


}]));

app.controller('NotepadsCtrl', INCLUDES.concat([function (sc, $filter,$http,$sce,api_service){
    sc.notepads = []
    sc.loading = true
    sc.selected = {}
    sc.loadingSalvar = false

    //api_service.getLogs().then((r)=>sc.logs = r)
    sc.updateNotepads = ()=>{
        sc.loading = true
        api_service.getNotepads().then((r)=>{sc.notepads = r;sc.loading=false})
    }

    sc.select =(item)=>{
        sc.selected = item
    } 

    sc.novaLista = ()=>{

        if(sc.listName == null || sc.listName.trim() == ""){
            toastr.warning('Insira o nome da lista!');
            return
        }

        sc.loadingSalvar = true
        api_service.newNotepad({name:sc.listName.trim()}).then((r)=>{
            print(r)
            sc.loadingSalvar = false
            toastr.success('Lista adcionada com sucesso!');
            sc.listName = ""
            sc.updateNotepads()
            $("#modal-novaLista").modal("hide")

        }).catch(()=>sc.loadingSalvar = false)

    }

    sc.updateNotepads()

}]));

SOCKET = null
app.controller('DashboardCtrl', INCLUDES.concat(['locador_svc',function (sc, $filter,$http,$sce,api_service,locador_svc){
    sc.FROMSOCKET = {cadastrados:0,online:0,offline:0}
    socket = io();
    SOCKET = socket

    socket.on('refreshDashboard', function(msg) {
      sc.FROMSOCKET = msg
      sc.$apply();
    });
    socket.on('disconnect', function(msg) {
        print("caiu")
    });

    sc.refresh = ()=> socket.emit("forceRefreshDashBoard")

    socket.emit("refreshDashboard")

}]));

app.controller('LocadoresCtrl', INCLUDES.concat(['locador_svc',function (sc, $filter,$http,$sce,api_service,locador_svc){
    sc.documentos = []
    sc.lista = FROMBACKEND.lista
    sc.Selected = {}
    sc.temas = []
    sc.locadores = []
    sc.loading = true

    sc.select = (item)=>{
        sc.Selected = item
        sc.Selected.senha2 =  sc.Selected.senha
        sc.Selected.pessoa.documento = sc.documentos.filter((i)=>{if(i.id == item.pessoa.documento.id)return i})[0]
        // sc.Selected.id_sys_user = sc.locadores.filter((i)=>{if(i.id == item.sysUser.id)return i})[0]
        $('#toggle-demo').bootstrapToggle(item.ativo?'on':'off')
        // sc.token = ""
        $("#modal-editar").modal("show")
        print(item)
    }

    sc.salvaLocador = ()=>{
        novo = {
            id:sc.Selected.id,
            nome:sc.Selected.pessoa.nome,
            telefone:sc.Selected.pessoa.telefone,
            numero_documento:sc.Selected.pessoa.numero_documento,
            email:sc.Selected.pessoa.email,
            local:sc.Selected.local,
            endereco:sc.Selected.endereco,
            user_name:sc.Selected.username,
            senha:sc.Selected.senha,
            senha2:sc.Selected.senha2,
            id_doc_type:sc.Selected.pessoa.documento,
            ativo:sc.Selected.ativo,
            descricao:sc.Selected.descricao
        }
        console.log(novo)
        locador_svc.salvaLocador(novo).then((r)=>{
            toastr.success('Locador alterado com sucesso!');
        })
    }

    sc.openModal = ()=>$('#modal-novoTema').modal('show')

    api_service.getDocs().then((r)=>sc.documentos = r)
    api_service.getLocadores2(FROMBACKEND).then((r)=>{
        sc.locadores = r;
        sc.loading = false;
    }).catch(()=>sc.loading = false)

}]));

app.controller('UsuariosCtrl', INCLUDES.concat([function (sc, $filter,$http,$sce,api_service){
    sc.id_locador = FROMBACKEND.id_locador
    sc.id_user = FROMBACKEND.id_user
    sc.loading = true
    sc.lista = []
    sc.Selected = {}
    sc.usuarios = []
    sc.documentos = []

    api_service.getDocs().then((r)=>{sc.documentos = r})
    api_service.getUsuarios(FROMBACKEND).then((r)=>{
        sc.usuarios = r;
        sc.loading = false}
        ).catch(()=>sc.loading = false)

    //api_service.getMaquinaId(sc.idLista).then((r)=>sc.lista = r)

    sc.select = (item)=>{
        sc.Selected = item

        if(item.pessoa.documento)
        sc.Selected.pessoa.documento = sc.documentos.filter((i)=>{if(i.id == item.pessoa.documento.id)return i})[0]
        
        $('#toggle-demo').bootstrapToggle(item.ativo?'on':'off')
        
        $("#modal-editar").modal("show")

    }


    sc.salvaUsuario = ()=>{
        obj = JSON.parse(JSON.stringify(sc.Selected));
        
        notEmpty = ["pessoa.nome","pessoa.telefone","pessoa.numero_documento","pessoa.email","numero_cartao"]
        for(var i=0;i<notEmpty.length;i++){
            ob = eval("obj." + notEmpty[i])
            if(ob == null || ob.trim() == ''){
                return toastr.warning('o campo ' + notEmpty[i] +  ' não pode estar vazio');
            }
        }
        
        if(obj.pessoa.documento == null){
            return toastr.warning('o campo tipo_do_documento não pode estar vazio');
        }

        obj2 = {
            nome:obj.pessoa.nome,
            telefone:obj.pessoa.telefone,
            email:obj.pessoa.email,
            numero_cartao:obj.numero_cartao,
            id_doc_type:obj.pessoa.documento.id,
            numero_documento:obj.pessoa.numero_documento,
            freeplay_data_exp:obj.freeplay_data_exp == null?"":obj.freeplay_data_exp,
            ativo:obj.ativo
        }
        console.log(obj2)
        
        api_service.putUsuarios(obj2).then(r =>{
            toastr.success('Usuario atualizado com sucesso!');
        })
    }
    

}]));

app.controller('NovoUsuarioCtrl', INCLUDES.concat([function (sc, $filter,$http,$sce,api_service){
    sc.documentos = []
    sc.Usuario = {nome:null,telefone:null,email:null,numero_cartao:null,id_doc_type:null,numero_documento:null,ativo:false}
    sc.loading = false

    api_service.getDocs().then((r)=>sc.documentos = r)

    sc.cadastraUsuario = ()=>{
        obj = JSON.parse(JSON.stringify(sc.Usuario));
        
        notEmpty = ["nome","telefone","numero_documento","email","numero_cartao"]
        for(var i=0;i<notEmpty.length;i++){
            if(obj[notEmpty[i]] == null || obj[notEmpty[i]].trim() == ''){
                return toastr.warning('o campo ' + notEmpty[i] +  ' não pode estar vazio');
            }
        }
        if(obj.id_doc_type == null){
            return toastr.warning('o campo tipo_do_documento não pode estar vazio');
        }
        obj.id_doc_type = obj.id_doc_type.id

        sc.loading = true
        api_service.postUsuarios(obj).then((r)=>{
            sc.loading = false
            sc.Usuario = {nome:null,telefone:null,email:null,numero_cartao:null,id_doc_type:null,numero_documento:null,ativo:false}
            toastr.success('Usuario cadastrado com sucesso!');
        }).catch(()=>sc.loading = false)
    }

}]));

app.controller('CarregarCtrl', INCLUDES.concat([function (sc, $filter,$http,$sce,api_service){
    sc.usuarios = []
    sc.valor = null
    sc.selected = null
    sc.loading = true
    sc.loadingButton = false
    sc.free = null

    api_service.getUsuarios2().then((r)=>{
        sc.usuarios = r
        sc.loading = false
    })


    sc.carregar = ()=>{

        if(!(sc.valor || sc.free)){
            return toastr.error("valor inválido");
        }

        sc.valor += 0 //transforma null em 0
        sc.free += 0 //transforma null em 0
        console.log(sc.free)

        sc.loadingButton = true //logo carregando e desabilita o botao
        data={id_user:sc.selected.id,credito:sc.valor,free_play_days:sc.free}
        api_service.creditUsuarios(data).then((r)=>{
            toastr.success(r);
            sc.selected.credito += sc.valor
            sc.loadingButton = false //logo carregando e habilita o botao
            sc.selected = null
            sc.valor = 0
            sc.free = 0
        }).catch(()=>sc.loadingButton = false)
    }

    sc.$watch('documento', function(newValue, oldValue) {
        if(newValue!==oldValue) {
            sc.selected = sc.usuarios.filter(item=>{
                if(item.pessoa.numero_documento == newValue)return item
            })
            sc.selected = sc.selected.length?sc.selected[0]:null
        } 
     });
   

}]));

app.filter('filterJson', function () {

    var x = function (original, campo,valor) {
        lst = original.filter(function(a){if(eval("a." + campo) == valor){return eval("a." + campo)}})
        return lst;
    };
    return x;
});


app.directive("editarMaquina", function() {
    function link (scope, element, attrs) {
        scope.t = "hehe"
    }
    return {
        restrict: 'E',
        link: link,
        templateUrl: 'static/angularJs/diretivas/editarMaquina/editarMaquina.html'
    };
});


function removeItemArrray(arr, value) {
    var index = arr.indexOf(value);
    var arr2 = arr.slice()
    if (index > -1) {
    arr2.splice(index, 1);
    }
    return arr2;
    }
    
function closeModal(){
document.querySelector("#myTab>li>a").click()
}

print = (x)=>console.log(x)


function getDate(){
    var today = new Date();
    var dd = String(today.getDate()).padStart(2, '0');
    var mm = String(today.getMonth() + 1).padStart(2, '0'); //January is 0!
    var yyyy = today.getFullYear();

    today = dd + '/' + mm + '/' + yyyy;
    return today
}

var tryReconnect = function(){

    if (socketClient.connected === false) {
        // use a connect() or reconnect() here if you want
        socketClient.socket.connect()
   }
}