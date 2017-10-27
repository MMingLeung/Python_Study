/**
 * Created by mingleung on 2017/10/4.
 */
//    自执行的函数
(function (jq) {
    var SEARCH_FLAG = true;
    var GLOBAL_DICT = {};
    var REFREASH = false;
    var CREATE_DICT = {};

    String.prototype.format = function (arg) {

        return this.replace(/\{(\w+)\}/g, function (k, kk) {
            return arg[kk];
        });
    };

    // 返回搜索条件
    function getSearchCondition() {
        var condition = {};
        $('.search-list').find('input[type="text"],select').each(function () {
            //select框或者input框
            /*{
            cabinet_num__contains:["A"]
            device_status_id:["1"]
            device_type_id:["1"] }
             */
            var name = $(this).attr('name');
            var value = $(this).val();
            if (condition[name]){
                condition[name].push(value)
            }else{
                condition[name] = [value];
            }
        });
        return condition
    }

    function initial(url) {
        // 执行函数，获取当前搜索条件
        if (REFREASH){
            var searchCondition = {}
        }else {
             var searchCondition = getSearchCondition();
            // console.log(searchCondition);
        }

        $.ajax({
            url: url,
            type: 'GET',  //获取数据
            dataType: 'JSON',
            //{"device_type_id":["1","2"],"device_status_id":["1"],"cabinet_num__contains":["A"]}
            data:{condition:JSON.stringify(searchCondition)},
            success: function (res) {
                $.each(res.global_dict, function (k, v) {
                    GLOBAL_DICT[k] = v
                });
                /*
                 'table_config': table_config,
                 'server_list': list(v),
                 'global_dict': {
                 'device_status_choices': models.Asset.device_status_choices,
                 'device_type_choices': models.Asset.device_type_choices,
                 }
                 */

                initTableHeader(res.table_config);
                initTableBody(res.server_list, res.table_config);
                initSearch(res.search_config);
                initMotai(res.motai_config);

            }
        })
    }

    function initMotai(motaiConfig) {

        $.each(motaiConfig, function (k, v) {
            CREATE_DICT[v.q] = "";
            var div = document.createElement('div');
            div.setAttribute('class', 'form-group');
            var label = document.createElement('label');
            label.innerText = v.title;
            var name = v.attrs.name;
            var type = v.attrs.type;

            if (type == 'input') {
                var a = document.createElement(type);
                $.each(v.attrs, function (k, v) {
                    a.setAttribute(k, v)
                });
                $(div).append(label);
                $(div).append(a);
                $('#AddFieldInner').append(div);
            } else if (type == 'select') {

                // console.log(v.attrs);
                var globalName = v.attrs.globalKey;

                var sel = document.createElement('select');
                $.each(v.attrs, function (k, v) {
                    sel.setAttribute(k, v)
                });
                $.each(GLOBAL_DICT[globalName], function (k, v) {
                    var op = document.createElement('option');
                    $(op).text(v[1]);
                    $(op).val(v[0]);
                    $(sel).append(op);
                });
                $(div).append(label);
                $(div).append(sel);
                $('#AddFieldInner').append(div);
            }
            else if (type == 'checkbox') {
                var globalName = v.attrs.globalKey;
                var ul = document.createElement('ul');
                ul.setAttribute('id', 'tags');
                $.each(GLOBAL_DICT[globalName], function (k,v) {
                    var chk = document.createElement('input');
                    var li = document.createElement('li');
                    var label = document.createElement('label');
                    li.setAttribute('style','display:inline;padding:15px');
                    chk.setAttribute('type', type);
                    chk.setAttribute('class', 'form-control');
                    chk.setAttribute('name', name);
                    label.innerText = v[1];
                    $(chk).val(v[0]);
                    $(label).append(chk);
                    $(li).append(label);
                    $(ul).append(li);
                });
                $(div).append(label);
                $(div).append(ul);
                $('#AddFieldInner').append(div);
            }
        });
    }


    function initSearch(searchConfig) {
        //只需要生成一次
        if (searchConfig && SEARCH_FLAG) {
            SEARCH_FLAG = false;
            //找到searchArea ul
            $.each(searchConfig, function (k, v) {
                /*
                 search_config = [
                 {'name': 'carbinet_num', 'text': '机柜号', 'condition_type': 'input'},
                 {'name': 'device_type_id', 'text': '资产类型', 'condition_type': 'select', 'global_name': 'device_type_choices'},
                 {'name': 'device_status_id', 'text': '资产状态', 'condition_type': 'select',
                 'global_name': 'device_status_choices'},
                 ]
                 */
                // if(k == 0){
                //     $('.searchDefault').text(v.text)
                // }

                var li = document.createElement('li');
                var a = document.createElement('a');
                a.innerHTML = v.text;
                $(li).append(a);
                $(li).attr('condition_type', v.condition_type);
                $(li).attr('name', v.name);
                if (v.condition_type == 'select') {
                    $(li).attr('global_name', v.global_name);
                }
                $('.searchArea ul').append(li)

            });

            //初始化默认配置
            //searchConfig[0]初始化

            $('.search-item .searchDefault').text(searchConfig[0].text);
            if (searchConfig[0].condition_type == 'select') {
                var sel = document.createElement('select');
                $(sel).attr('class', 'form-control');
                $(sel).attr('name', searchConfig[0].name);
                $.each(GLOBAL_DICT[searchConfig[0].global_name], function (k, v) {
                    var op = document.createElement('option');
                    $(op).text(v[1]);
                    $(op).val(v[0]);
                    $(sel).append(op);
                });
                $('.input-group').append(sel)
            } else {
                var inp = document.createElement('input');
                $(inp).attr('name', searchConfig[0].name);
                $(inp).attr('type', 'text');
                $(inp).attr('class', 'form-control');
                $('.input-group').append(inp)
            }

        }
    }

    function initTableHeader(tableConfig) {
        /*
         {title: "ID", q: "id"}
         {title: "主机名", q: "hostname"}
         */
        $('#tbHeader').empty();
        var tr = document.createElement('tr');
        $.each(tableConfig, function (k, v) {
            if (v.display) {
                var tag = document.createElement('th');
                tag.innerHTML = v.title;
                $(tr).append(tag)
            }
        });
        $('#tbHeader').append(tr);
    }

    function initTableBody(serverList, tableConfig) {

        $('#tbBody').empty();
        $.each(serverList, function (k, row) {
            /*
             *  k = 0 row = {hostname: "c1.com", id: 1, create_at: "2017-10-02 05:00:55"}
             0:{hostname: "c1.com", id: 1, create_at: "2017-10-02 05:00:55"}
             * */
            //
            var tr = document.createElement('tr');
            tr.setAttribute("nid", row.id);
            $.each(tableConfig, function (kk, rrow) {
                /*
                 k = 0: row = {q: "id", title: "ID"} // row.q = id
                 1:{q: "hostname", title: "主机名"}     // row.q = hostname
                 2:{q: "create_at", title: "创建时间"}
                 */

                if (rrow.display) {

                    var td = document.createElement('td');
                    // 在td标签添加内容
                    //            if(rrow['q'])//}
                    //                td.innerHTML = row[rrow.q];
                    //            }else//}
                    //                td.innerHTML = rrow.text;
                    //            #}
                    //              rrow.text.tpl: 'aa{n1}ddd'#}
                    //              rrow.text.kwargs: {'n1':'123'}#}
                    //             rrow.text.kwargs: {'n1':'@id', 'n2':'123'}#}


                    $.each(rrow.attrs, function (atkey, atval) {
                        //判断如果是@ + XX取真实的值
                        if (atval[0] == '@') {
                            //取到id的值
                            td.setAttribute(atkey, row[atval.substring(1, atval.length)])
                        } else {
                            td.setAttribute(atkey, atval)
                        }

                    });


                    //@id变更 rrow.text.kwargs: {'n1':'1', 'n2':'123'}#}
                    var newKwargs = {};
                    $.each(rrow.text.kwargs, function (j, k) {

                        var aValue = k;

                        //'kwargs': {'n1': '@@device_type_choices'}
                        if (k.substring(0, 2) == '@@') {
                            var global_key = k.substring(2, k.length);
                            //device_type_id
                            //获取device_type_id的值
                            var did = row[rrow.q];
                            $.each(GLOBAL_DICT[global_key], function (gk, gv) {
                                if (gv[0] == did) {
                                    aValue = gv[1];
                                }
                            })
                        }
                        else if (k[0] == '@') {
                            //取到id的值
                            aValue = row[k.substring(1, k.length)]
                        }

                        newKwargs[j] = aValue;
                    });

                    var newText = rrow.text.tpl.format(newKwargs);
                    td.innerHTML = newText;
                    tr.append(td)
                }
            });

            $('#tbBody').append(tr);

        });

    }

    function trIntoEdit($tr) {
        //找到所有的td标签且edit-enable="true"
        $tr.find('td[edit-enable="true"]').each(function () {

            var editType = $(this).attr('edit-type');
            if (editType == 'select') {
                //生成下拉框:找到数据源

                //默认选中原来的值
                var origin = $(this).attr('origin'); //原来的值

                var deviceTypeChoices = GLOBAL_DICT[$(this).attr('global-key')];
                //生成select标签
                var selectTag = document.createElement('select');
                $.each(deviceTypeChoices, function (k, v) {
                    var option = document.createElement('option');
                    $(option).text(v[1]);
                    $(option).val(v[0]);
                    if (v[0] == origin) {
                        $(option).prop('selected', true);
                    }

                    $(selectTag).append(option)

                });

                //放到td中
                $(this).html(selectTag);
            } else {
                var v1 = $(this).text(); //循环的每一个td,获取文本信息
                var inp = document.createElement('input');
                $(inp).val(v1);
                //input标签替换原来的内容
                $(this).html(inp);
            }

        })
    }

    function trOutEdit($tr) {
        //找到所有的td标签且edit-enable="true"
        $tr.find('td[edit-enable="true"]').each(function () {
            var editType = $(this).attr('edit-type');
            if (editType == 'select') {
                //DOM对象
                var option = $(this).find('select')[0].selectedOptions;
                $(this).html($(option).text());

                //用于编辑保存时对比旧值
                $(this).attr('newOrigin', $(option).val())

            } else {
                var inputVal = $(this).find('input').val();
                //input标签替换原来的内容
                $(this).html(inputVal);
            }
        })
    }

    function addFadeOut(){
        $('#AddFieldOuter').fadeOut(500);
        $('#AddFieldInner').fadeOut(500);
    }
    function addFadeIn(){
              $('#AddFieldOuter').fadeIn(500);
            $('#AddFieldInner').fadeIn(500);
    }

    jq.extend({
        xx: function (url) {
            initial(url);
            //对所有的checkbox绑定事件

            $("#tbBody").on('click', ':checkbox', function () {
                //alert($(this).val()); //this当前checkbox标签
                //检测是否已经被选中
                if ($('#InOutEditMode').hasClass('btn-warning')) {
                    if ($(this).prop('checked')) {
                        //进入编辑模式
                        // tr jquery对象
                        var $tr = $(this).parent().parent();
                        trIntoEdit($tr);
                    } else {
                        //退出编辑模式
                        var $tr = $(this).parent().parent();
                        trOutEdit($tr);

                    }
                }

            });

            //对所有按钮绑定事件

            $('#checkAll').click(function () {
                // $('#tbBody').find(':checkbox').prop('checked', true)
                // //进入编辑模式
                // $('#tbBody').find('tr').each(function () {
                //     trIntoEdit($(this));
                // })
                //
                if ($('#InOutEditMode').hasClass('btn-warning')) {
                    $('#tbBody').find(':checkbox').each(function () {
                        if (!$(this).prop('checked')) {
                            var $tr = $(this).parent().parent();
                            trIntoEdit($tr);
                            $(this).prop('checked', true)
                        }
                    })
                } else {
                    $('#tbBody').find(':checkbox').prop('checked', true)
                }

            });
            $('#checkReverse').click(function () {
                if ($('#InOutEditMode').hasClass('btn-warning')) {
                    $('#tbBody').find(':checkbox').each(function () {
                        var $tr = $(this).parent().parent();
                        if ($(this).prop('checked')) {
                            var $tr = $(this).parent().parent();
                            trOutEdit($tr);
                            $(this).prop('checked', false)
                        } else {
                            if (!$(this).prop('checked')) {
                                var $tr = $(this).parent().parent();
                                trIntoEdit($tr);
                                $(this).prop('checked', true)
                            }

                        }
                    })
                } else {
                    $('#tbBody').find(':checkbox').each(function () {
                        var $tr = $(this).parent().parent();
                        if ($(this).prop('checked')) {
                            $(this).prop('checked', false)
                        } else {
                            if (!$(this).prop('checked')) {
                                $(this).prop('checked', true)
                            }

                        }
                    })

                }
            });
            $('#checkCancel').click(function () {
                // $('#tbBody').find(':checkbox').prop('checked', false)
                // //退出编辑模式
                // $('#tbBody').find('tr').each(function () {
                //     trIntoEdit($(this));
                // })
                if ($('#InOutEditMode').hasClass('btn-warning')) {
                    $('#tbBody').find(':checkbox').each(function () {
                        if ($(this).prop('checked')) {
                            var $tr = $(this).parent().parent();
                            trOutEdit($tr);
                            $(this).prop('checked', false)
                        }
                    })
                } else {
                    $('#tbBody').find(':checkbox').prop('checked', false)
                }
            });
            $('#InOutEditMode').click(function () {
                if ($(this).hasClass('btn-warning')) {
                    //exit edit
                    $(this).removeClass('btn-warning');
                    $(this).text('进入编辑模式');

                    $("#tbBody").find(':checkbox').each(function () {
                        if ($(this).prop('checked')) {

                            var $tr = $(this).parent().parent();
                            trOutEdit($tr);
                        }
                    });

                } else {
                    //enter edit

                    $(this).addClass('btn-warning');
                    $(this).text('退出编辑模式');

                    $("#tbBody").find(':checkbox').each(function () {
                        if ($(this).prop('checked')) {

                            var $tr = $(this).parent().parent();
                            trIntoEdit($tr);
                        }
                    });
                }

            });
            $('#mulDelete').click(function () {
                //找到被选中的
                var idList = [];
                $('#tbBody').find(':checked').each(function () {
                    idList.push($(this).val());

                });
                $.ajax({
                    url: url,
                    type: 'delete',
                    data: JSON.stringify(idList),
                    success: function (arg) {
                        // console.log(arg)
                    }
                })

            });
            $('#refresh').click(function () {
                REFREASH = true;
                initial(url);

            });
            $('#checkSave').click(function () {
                //退出编辑模式

                if ($('#InOutEditMode').hasClass('btn-warning')) {
                    $('#tbBody').find(':checkbox').each(function () {
                        if ($(this).prop('checked')) {
                            var $tr = $(this).parent().parent();
                            trOutEdit($tr);
                            $(this).prop('checked', false)
                        }
                    })
                }

                //获取数据发到后台
                var all_list = [];
                $('#tbBody').children().each(function () {
                    //tr对象
                    var $tr = $(this);
                    var nid = $tr.attr('nid');
                    //找edit-enable = true
                    var row_dict = {};
                    var flag = false;
                    $tr.children().each(function () {
                        if ($(this).attr('edit-enable')) {
                            if ($(this).attr('edit-type') == 'select') {
                                //下拉框的保存
                                var newData = $(this).attr('newOrigin');
                                var oldData = $(this).attr('origin');
                                if (newData) {
                                    if (newData != oldData) {
                                        var name = $(this).attr('name');
                                        row_dict[name] = newData;
                                        flag = true;
                                    }
                                }
                            } else {
                                //input框的保存
                                var newData = $(this).text();
                                var oldData = $(this).attr('origin');

                                if (newData != oldData) {
                                    var name = $(this).attr('name');
                                    row_dict[name] = newData;
                                    flag = true;
                                }
                            }
                        }
                    });

                    if (flag) {
                        row_dict['id'] = nid;

                    }
                    all_list.push(row_dict);


                });

                //ajax 请求
                $.ajax({
                    url: url,
                    type: 'PUT',
                    data: JSON.stringify(all_list),
                    success: function (arg) {
                        // console.log(arg)
                    }

                })

            });
            //右边输入框每次点击都要更改
            $('.search-list').on('click', 'li', function () {
                //文本信息
                var wenben = $(this).text();
                var name = $(this).attr('name');
                var globalName = $(this).attr('global_name');
                var conditinType = $(this).attr('condition_type');

                //选择后把显示文本替换
                // $(".searchDefault").text(wenben);
                //li父节点ul的上一个节点寻找.searchDefault改变文本
                $(this).parent().prev().find('.searchDefault').text(wenben);
                if (conditinType == 'select') {
                    //输入框
                    var sel = document.createElement('select');
                    //列表[1,xx],[2,bb],生成option
                    $(sel).attr('class', 'form-control');
                    $(sel).attr('name', name);
                    $.each(GLOBAL_DICT[globalName], function (k, v) {
                        var op = document.createElement('option');
                        $(op).text(v[1]);
                        $(op).val(v[0]);
                        $(sel).append(op);
                    });
                    $(this).parent().parent().next().remove();
                    $(this).parent().parent().after(sel);
                } else {

                    var inp = document.createElement('input');
                    $(inp).attr('class', 'form-control');
                    $(inp).attr('name', name);
                    $(inp).attr('type', 'text');
                    $(this).parent().parent().next().remove();
                    $(this).parent().parent().after(inp);

                }


            });
            $('.search-list').on('click', '.addSearchCondition', function () {
                //找到search-item 拷贝新的搜索项
                var newSearcheItem = $(this).parent().parent().clone();
                $(newSearcheItem).find('.addSearchCondition span').removeClass('glyphicon glyphicon-plus').addClass('glyphicon glyphicon-minus');
                $(newSearcheItem).find('.addSearchCondition').addClass('del').removeClass("addSearchCondition");
                $('.search-list').append(newSearcheItem);

            });
            $('.search-list').on('click', '.del', function () {
                //由当前按钮找到整个search-item 删除
                $(this).parent().parent().remove()
            });
            $('#doSearch').click(function () {

                REFREASH = false;
                //所有条件发到后台
                initial(url)

            });
            $('#AddFieldSubmit').click(function () {
                var cabinet_num = $('input[name=cabinet_num]').val();
                var cabinet_order = $('input[name=cabinet_order]').val();
                var idc = $('#idc')[0].selectedIndex + 1;
                var device_type_id = $('#device_type_id')[0].selectedIndex + 1;
                var device_status_id = $('#device_status_id')[0].selectedIndex + 1;
                var business_unit = $('#business_unit')[0].selectedIndex + 1;
                var tag = [];
                var tags = $('#tags').find('input[type="checkbox"]');
                $.each(tags,function (k,v) {
                    if(v.checked){
                        tag.push($(v).val());
                    }
                });
                // console.log(tagsList);
                // console.log(cabinet_num, cabinet_order, idc)
                var create_dict = {
                    "cabinet_num":cabinet_num,
                    "cabinet_order":cabinet_order,
                    "idc_id":idc,
                    "device_type_id":device_type_id,
                    "device_status_id":device_status_id,
                    "business_unit_id":business_unit,
                    "tag":tag
                };
                $.ajax({
                    url:url,
                    type:'POST',
                    dataType:'JSON',
                    data:{create_dict:JSON.stringify(create_dict)},
                    success:function (res) {
                        if (!res.status){
                            $('#errorMsg').text(res.data);
                        }else {
                            addFadeOut();
                            REFREASH = true;
                            initial(url);
                        }
                    }
                })
            });
            $('#AddFieldCancel').click(function(){
                addFadeOut();
            });
            $('#add').click(function () {
                addFadeIn();
            })
        }
    })

})(jQuery);