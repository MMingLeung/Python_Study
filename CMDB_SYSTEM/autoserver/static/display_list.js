/**
 * Created by mingleung on 2017/12/29.
 */


(function (jq) {
    var SEARCH_FLAG = true;
    var GLOBAL_DICT = {};
    var FLASH_FLAG = false;
    var csrf_token= $("input[name='csrfmiddlewaretoken']").val();

    function initialHeaders(tableConfig) {
        $('#tbHead').empty();
        var tr = document.createElement('tr');
        $.each(tableConfig, function (k, v) {
            /*
             0:{q: "id", title: "ID"}
             1:{q: "hostname", title: "主机名"}
             * */
            if (v.disable) {
                var th = document.createElement('th');
                th.innerHTML = v.title;
                tr.append(th)
            }

        });
        $('#tbHead').append(tr);
    }

    function initialBody(tableConfig, serverList) {
        String.prototype.format = function (args) {
            return this.replace(/\{(\w+)\}/g, function (k, kk) {
                return args[kk];
            })
        };
        $('#tbBody').empty();
        $.each(serverList, function (k, row) {
            /*
             0:{hostname: "c1.com", id: 1}
             **/
            var tr = document.createElement('tr');
            tr.setAttribute('nid', row['id']);
            $.each(tableConfig, function (tck, tcv) {
                if (tcv.disable) {
                    var content = tcv.text.tpl;
                    var td = document.createElement('td');
                    $.each(tcv.text.kwargs, function (kwargKey, kwargValue) {
                        var valDict = {};
                        var trueValue = kwargValue;

                        if (kwargValue.substring(0, 2) == '@@') {
                            // 'kwargs':{'n1':'@@device_status_id'}
                            var gbKey = kwargValue.substring(2, kwargValue.length);
                            $.each(GLOBAL_DICT[gbKey], function (gdKey, gdValue) {
                                if (gdValue[0] == row[tcv.q]) {
                                    trueValue = gdValue[1];
                                }
                            })
                        }
                        else if (kwargValue.substring(0, 1) == '@') {
                            trueValue = row[kwargValue.substring(1, kwargValue.length)];
                        }
                        valDict[kwargKey] = trueValue;
                        td.innerHTML = content.format(valDict);
                    });
                    $.each(tcv.attrs, function (attrKey, attrValue) {
                        var trueValue = attrValue;
                        if (attrValue.substring(0, 2) == '@@') {
                            var globalDictKey = attrValue.substring(2, attrValue.length);
                            $.each(GLOBAL_DICT[globalDictKey], function (gbKey, gbValue) {
                                if (gbValue[0] == row[tcv.q]) {
                                    trueValue = gbValue[1];
                                }
                            })
                        }
                        else if (attrValue.substring(0, 1) == '@') {
                            trueValue = row[attrValue.substring(1, attrValue.length)]
                        }
                        td.setAttribute(attrKey, trueValue)
                    })
                }
                $(tr).append(td);
            });
            $('#tbBody').append(tr);
        })
    }

    function getSearchCondition() {
        var condition = {};
        $('.searchList').find('input[type="text"], select').each(function () {
            // $(this)
            var name = $(this).attr('name');
            var value = $(this).val();
            // 机柜号:[1,2,3] 是"或"的关系
            if (condition[name]) {
                condition[name].push(value);
            } else {
                condition[name] = [value];
            }
        });
        return condition
    }

    function initial(url) {
        // 执行一个函数，获取当前搜索条件，当作参数传到后台
        if(FLASH_FLAG){
             var searchCondition = {};
             FLASH_FLAG = false
        }else {
             var searchCondition = getSearchCondition();
        }


        $.ajax({
            url: url,
            type: 'GET',
            dataType: 'JSON',
            data:{condition:JSON.stringify(searchCondition)},
            success: function (arg) {
                $.each(arg.global_dict, function (key, value) {
                    GLOBAL_DICT[key] = value;
                });
                initialHeaders(arg.table_config);
                initialBody(arg.table_config, arg.server_list);
                initialSearch(arg.search_config)
            }
        });
    }

    function initialSearch(searchConfig) {
        if (searchConfig && SEARCH_FLAG) {
            SEARCH_FLAG = false;

            // 找到searchArea ul放入li
            $.each(searchConfig, function (k, v) {
                var li = document.createElement('li');
                li.setAttribute('search_type', v.search_type);
                li.setAttribute('name', v.name);
                if (v.search_type == 'select') {
                    li.setAttribute('global_key', v.global_key);
                }
                var a = document.createElement('a');
                a.innerHTML = v.text;
                li.append(a);
                $('.searchArea ul').append(li);
            });

            $('#defaultSearch').text(searchConfig[0].text);

            if (searchConfig[0].search_type == 'select') {
                var sel = document.createElement('select');
                $(sel).attr('class', 'form-control');
                $.each(GLOBAL_DICT[searchConfig[0].global_key], function (k, v) {
                    var optTag = document.createElement('option');
                    $(optTag).text(v[1]);
                    $(optTag).val(v[0]);
                    $(sel).append(optTag);
                });
                $('.input-group').append(sel);
            } else {
                var inp = document.createElement('input');
                $(inp).attr('name', searchConfig[0].name);
                $(inp).attr('search_type', searchConfig[0].search_type);
                $(inp).attr('type', 'text');
                $(inp).addClass('form-control');
                $('.input-group').append(inp)
            }


        }
    }

    function intoEdit($tr) {
        // $tr： 一行数据
        $tr.find('td[edit-enable="true"]').each(function () {
            var editType = $(this).attr('edit-type');
            if (editType == 'select') {
                // 生成下拉框,需要数据
                var deviceTypeChoices = GLOBAL_DICT[$(this).attr('global_key')];
                // 显示默认值
                var selectTag = document.createElement('select');
                var originVal = $(this).attr('origin');
                $.each(deviceTypeChoices, function (k, v) {
                    // v[0]: id
                    // v[1]: value
                    var optionTag = document.createElement('option');
                    $(optionTag).text(v[1]);
                    $(optionTag).val(v[0]);
                    $(selectTag).append(optionTag);

                    // 默认选中
                    if (v[0] == originVal) {
                        $(optionTag).prop('selected', true)
                    }

                });
                $(this).html(selectTag)
            } else {
                var v1 = $(this).text();
                var ipt = document.createElement('input');
                $(ipt).val(v1);
                $(this).html(ipt)
            }

        })
    }

    function outEdit($tr) {
        // $tr： 一行数据
        $tr.find('td[edit-enable="true"]').each(function () {
            var editType = $(this).attr('edit-type');
            if (editType == 'select') {
                var optionTag = $(this).find('select')[0].selectedOptions;
                var txt = $(optionTag).text();
                var val = $(optionTag).val();
                $(this).attr('new-origin', val);
                $(this).text(txt);
                $(this).val(val);


            } else {
                var v1 = $(this).find('input').val();
                $(this).html(v1);
            }

        })
    }

    jq.extend({
            xx: function (url) {
                initial(url);

                $('#tbBody').on('click', ':checkbox', function () {
                    // 选中的进入编辑模式
                    if ($('#checkInOut').hasClass('btn-warning')) {
                        if ($(this).prop('checked')) {
                            intoEdit($(this).parent().parent());
                        }
                        // 没有选中的退出编辑模式
                        else {
                            outEdit($(this).parent().parent());
                        }
                    }
                });

                $('#checkAll').click(function () {
                    /*
                     $('#tbBody').find(':checkbox').prop('checked', true);
                     $('#tbBody').find('tr').each(function () {
                     intoEdit($(this));
                     })
                     */
                    if ($('#checkInOut').hasClass('btn-warning')) {
                        $('#tbBody').find(':checkbox').each(function () {
                            if (!$(this).prop('checked')) {
                                // 此处this是checkbox
                                var $tr = $(this).parent().parent();
                                intoEdit($tr);
                                $(this).prop('checked', true);
                            }
                        });
                    }
                    else {
                        $('#tbBody').find(':checkbox').each(function () {
                            if (!$(this).prop('checked')) {
                                // 此处this是checkbox
                                $(this).prop('checked', true);
                            }
                        });
                    }

                });

                $('#checkReverse').click(function () {

                    $('#tbBody').find(':checkbox').each(function () {
                        if ($('#checkInOut').hasClass('btn-warning')) {
                            if ($(this).prop('checked')) {
                                // 此处this是checkbox

                                var $tr = $(this).parent().parent();
                                outEdit($tr);
                                $(this).prop('checked', false);
                            } else {
                                var $tr = $(this).parent().parent();
                                intoEdit($tr);
                                $(this).prop('checked', true);
                            }
                        } else {
                            if ($(this).prop('checked')) {
                                // 此处this是checkbox
                                var $tr = $(this).parent().parent();
                                $(this).prop('checked', false);
                            } else {
                                var $tr = $(this).parent().parent();
                                $(this).prop('checked', true);
                            }
                        }


                    });

                });

                $('#checkCancel').click(function () {
                    if ($('#checkInOut').hasClass('btn-warning')) {
                        $('#tbBody').find(':checkbox').each(function () {
                            if ($(this).prop('checked')) {
                                // 此处this是checkbox
                                var $tr = $(this).parent().parent();
                                outEdit($tr);
                                $(this).prop('checked', false);
                            }
                        });
                    } else {
                        $('#tbBody').find(':checkbox').each(function () {
                            if ($(this).prop('checked')) {
                                // 此处this是checkbox
                                $(this).prop('checked', false);
                            }
                        });
                    }

                });

                $('#checkInOut').click(function () {
                    if ($(this).hasClass('btn-warning')) {
                        $(this).removeClass('btn-warning');
                        $(this).text('进入编辑模式');
                        $('#tbBody').find(':checkbox').each(function () {
                            if ($(this).prop('checked')) {
                                // 此处this是checkbox
                                var $tr = $(this).parent().parent();
                                outEdit($tr);
                                $(this).prop('checked', false);
                            }
                        });
                    } else {
                        $(this).addClass('btn-warning');
                        $(this).text('退出编辑模式');
                        $('#tbBody').find(':checkbox').each(function () {
                            if ($(this).prop('checked')) {
                                // 此处this是checkbox
                                var $tr = $(this).parent().parent();
                                intoEdit($tr);
                                $(this).prop('checked', true);
                            }
                        });

                    }
                });

                $('#checkDel').click(function () {
                    // :checked 找出被选中的checkbox
                    var idList = [];
                    $('#tbBody').find(':checked').each(function () {
                        idList.push($(this).val())
                    });
                    $.ajax({
                        url: url,
                        type: 'DELETE',
                        data: JSON.stringify(idList),
                        success: function (args) {

                        }

                    })
                });

                $('#checkFlash').click(function () {
                    FLASH_FLAG = true;
                    initial(url);
                });

                $('#checkSave').click(function () {
                    // 保存先退出编辑模式
                    if ($('#checkInOut').hasClass('btn-warning')) {
                        $('#tbBody').find(':checkbox').each(function () {
                            if ($(this).prop('checked')) {
                                // 此处this是checkbox
                                var $tr = $(this).parent().parent();
                                outEdit($tr);
                                $(this).prop('checked', false);
                            }
                        });

                        // 获取数据，发送ajax
                        var allList = [];
                        $('#tbBody').children('tr').each(function () {
                            // $(this): tr

                            var $tr = $(this);
                            var nid = $tr.attr('nid');
                            var rowDict = {};
                            var flag = false;
                            // 找能编辑的td
                            $tr.children().each(function () {
                                if ($(this).attr('edit-enable')) {
                                    if ($(this).attr('edit-type')) {
                                        var newData = $(this).attr('new-origin');
                                        var oldData = $(this).attr('origin');
                                        if (newData) {
                                            if (newData != oldData) {

                                                var name = $(this).attr('name');
                                                rowDict[name] = newData;
                                                flag = true
                                            }
                                        }
                                    }
                                    else {
                                        var newData = $(this).text();
                                        var oldData = $(this).attr('origin');
                                        if (newData != oldData) {

                                            var name = $(this).attr('name');
                                            rowDict[name] = newData;
                                            flag = true
                                        }
                                    }

                                }
                            });
                            // rowDict 要更新的key-value
                            if (flag) {
                                // 行的id
                                rowDict['id'] = nid;
                            }
                            allList.push(rowDict);

                        });
                        console.log(csrf_token);
                        $.ajax({
                            url: url + '?md=edit',
                            type: 'PUT',
                            data: JSON.stringify(allList),
                            headers : {'X-CSRFToken':csrf_token},
                            success: function (args) {
                                if (args == '无权限访问'){
                                    alert(args);
                                    location.reload();
                                }
                            }
                        })
                    }


                });

                $('.searchList').on('click', 'li', function () {
                    // 点击li执行函数
                    var txt = $(this).text();
                    var name = $(this).attr('name');
                    var searchType = $(this).attr('search_type');
                    var global_key = $(this).attr('global_key');

                    // 显示文本替换
                    // 找到ul --> pre
                    $(this).parent().prev().find('#defaultSearch').text(txt);


                    // 根据searchType更换输入框
                    if (searchType == 'select') {
                        // 输入的内容框

                        $(this).parent().parent().next().remove();
                        var sel = document.createElement('select');
                        $(sel).attr('class', 'form-control');
                        $(sel).attr('name', name);

                        $.each(GLOBAL_DICT[global_key], function (k, v) {
                            var optTag = document.createElement('option');
                            $(optTag).text(v[1]);
                            $(optTag).val(v[0]);
                            $(sel).append(optTag);
                        });

                        $(this).parent().parent().after(sel)

                    } else {
                        $(this).parent().parent().next().remove();
                        var inpt = document.createElement('input');
                        $(inpt).attr('class', 'form-control');
                        $(inpt).attr('name', name);
                        $(this).parent().parent().after(inpt)
                    }
                });

                // 委托绑定
                $('.searchList').on('click', '.add-search-condition', function () {
                    // 找到searchItem
                    var newSearchItem = $(this).parent().parent().clone();
                    $(newSearchItem).find('.add-search-condition span').removeClass('glyphicon glyphicon-plus').addClass('glyphicon glyphicon-minus');
                    $(newSearchItem).find('.add-search-condition').addClass('del-search-condition').removeClass('add-search-condition');
                    $('.searchList').append(newSearchItem);

                });

                $('.searchList').on('click', '.del-search-condition', function () {
                    $(this).parent().parent().remove();
                });

                $('#doSearch').click(function () {
                    // 获取所有searchList的条件


                    // 发送ajax请求


                    // initial初始化
                    initial(url);

                })
            }
        }
    )

})(jQuery);
