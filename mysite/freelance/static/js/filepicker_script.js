/**
 * Filepicker integration for JotForm
 * for more information visit doc page - https://www.filepicker.com/documentation/?v=v2
 * API version: v2
 * Last update: June 27, 2015
 * Author: Kenneth
 */
window._JF_filepickerIO = (function(){
    /**
     * Filepicker
     */
    return function Filepicker(options) {
        var params = {
            services: {
                defaultValue: [1,2,3,4,5,6,7,8,9,11,12,13,14,15,16,17,18,19,20],
                // default: [
                //     'BOX',
                //     'COMPUTER',
                //     'DROPBOX',
                //     'EVERNOTE',
                //     'FACEBOOK',
                //     'GMAIL',
                //     'IMAGE_SEARCH',
                //     'FLICKR',
                //     'FTP',
                //     'GITHUB',
                //     'GOOGLE_DRIVE',
                //     'SKYDRIVE',
                //     'PICASA',
                //     'URL',
                //     'WEBCAM',
                //     'INSTAGRAM',
                //     'VIDEO',
                //     'ALFRESCO',
                //     'CUSTOMSOURCE',
                //     'CLOUDDRIVE',
                //     'IMGUR',
                //     'CLOUDAPP',
                //     'CONVERT'
                // ],
                value: []
            },
            s3: {
                enabled: false,
                uploadPath: 'JotForm/{formID}/',
                accessType: 'public'
            },
            image: {
                crop: {},
                compress: {},
                resize: {}
            },

            allowDebug: false,
            formID: '',
            apiKey: '',
            qid: '',
            formTitle: '',
            containerType: 'window',
            maxFileSize: 1024000,
            extensions: '',
            mimetypes: false,
            multiple: false,

            pickerOptions: {},
            pickerOptionsS3: {},

            uploadedFiles: []
        };

        log('Filepicker options', options);
        log('Filepicker params', params);

        params.qid = options.qid;
        params.apiKey = options.apiKey;
        params.formTitle = String( (options.title) ? options.title : String(window.document.title) ).replace(/\s+/g, '_');
        params.multiple = options.multiple;

        //get services and some other options
        params.services.value = (options.services) ? options.services.split(",") : params.services.defaultValue;
        params.containerType = (options.modal.toLowerCase() === 'yes') ? 'modal' : params.containerType;
        params.maxFileSize = (options.maxsize) ? options.maxsize : params.maxFileSize;
        params.mimetypes = (options.mimetypes) ? options.mimetypes : params.mimetypes;
        params.openTo = options.openTo;

        // s3 details
        params.s3.enabled = (options.allowUploadToS3 && options.allowUploadToS3 === 'enabled') ? true : params.s3.enabled;
        params.s3.uploadPath = (options.s3UploadPath ) ? options.s3UploadPath : params.s3.uploadPath;
        params.s3.accessType = (options.s3UploadAccess ) ? options.s3UploadAccess : params.s3.accessType;

        // crop, compression && resize
        for ( var imagekey in params.image ) {
            var found = (imagekey in options && !!options[imagekey]) ? true : false;
            params.image[imagekey].enabled = found;

            // enabled if props set
            // set all image props to params
            if ( found ) {
                params.image[imagekey] = Object.extend(params.image[imagekey], options[imagekey]);
            }

        }

        // exposed functions
        this.init = init;

        /**
         * Initialization
         */
        function init() {

            // get previous links - edit mode
            handlePreviousValuesWhenEditMode();

            //set picker options
            params.pickerOptions = {
                mimetype: '*/*',
                container: params.containerType,
                services: params.services.value,
                openTo: params.openTo,
                maxSize: params.maxFileSize
            };

            // setup image handler
            imageManipulationSetup();

            // check file mimetypes
            // if mimetypes is not set to all
            if ( params.mimetypes && params.mimetypes !== '*/*' ) {
                //get mimetypes, remove spaces, and then turn to array [mimetype1, mimetype2, etc]
                var mime = params.mimetypes.replace(/\s+/gim, '').split(',');
                var mimeArray = [];

                for( var i = 0; i < mime.length; i++ ) {
                    mimeArray.push( String( mime[i] ) );
                }

                params.pickerOptions.mimetypes = mimeArray;
                mimeArray = null;
                mime = null;

                //remove single mimetype property
                delete params.pickerOptions.mimetype;

                log("Mimetype was set, updated picker options:", params.pickerOptions);
            }

            log("Current filepicker Options", params.pickerOptions);

            var filePickerElement = $("filePicker_" + params.qid);
            if ( filePickerElement ) {
                filePickerElement.observe("click", function(){
                    // get form id
                    params.formID = $$('input[name=formID]')[0].getValue();

                    // modify s3upload path if such keywords is found like {formID}, {form-title}
                    // only if enabled
                    params.s3.enabled && modifyS3Upload();

                    // set filepicker apikey
                    filepicker.setKey(params.apiKey);

                    // initiate uploading process
                    if ( params.multiple ) {
                        uploadMultiple();
                    } else {
                        uploadSingle();
                    }
                });
            } else {
                console.error("Missing filepicker button");
            }
        }

        /**
         * Correct s3 upload path and set the options for it
         */
        function correctAndSetS3UploadPath() {
            // fix start slash
            var s3UploadPath = params.s3.uploadPath;
            if ( s3UploadPath[0] !== '/' )  {
                s3UploadPath = '/' + s3UploadPath;
            }

            // fix last slash
            if ( s3UploadPath[s3UploadPath.length - 1] !== '/' ) {
                s3UploadPath += '/';
            }

            // set modified s3 upload path
            params.s3.uploadPath = s3UploadPath;
            params.pickerOptionsS3 = {
                location: 'S3',
                path: params.s3.uploadPath,
                access: params.s3.accessType
            };

            log('Uploaded to s3 initiated', params.pickerOptionsS3);
        }

        /**
         * Modify S3 upload path and then correct after
         */
        function modifyS3Upload() {
            //modifier list to replace such keyword found on a string
            var modifierList = [
                { reg:/\{formID\}/g, val: params.formID },
                { reg:/\{form\-title\}/g, val: params.formTitle }
            ];

            var s3UploadPath = params.s3.uploadPath;
            log("Old S3 Upload path", s3UploadPath);

            for( var i in modifierList ) {
                var obj = modifierList[ i ];

                if ( String(s3UploadPath).search(obj.reg) > -1  ) {
                    s3UploadPath = String(s3UploadPath).replace(obj.reg, obj.val);
                }
            }

            // set modified s3 upload path
            params.s3.uploadPath = s3UploadPath;
            log("Modified upload path", s3UploadPath);

            //correct and then set s3 upload path
            correctAndSetS3UploadPath();
        }

        /**
         * Set up image manipulations for the picker
         */
        function imageManipulationSetup() {
            // if crop image enabled, include CONVERT service
            // and insert cropRation option
            if ( params.image.crop.enabled ) {
                params.services.value.push('CONVERT');
                if ( params.image.crop.ratio !== 'none' ) {
                    params.pickerOptions.cropRatio = toDecimal(params.image.crop.ratio);
                }
            }

            // compression enabled, insert imageQuality to option
            if ( params.image.compress.enabled ) {
                params.pickerOptions.imageQuality = parseInt(params.image.compress.quality);
            }

            // resize setup
            // more info https://www.filepicker.com/documentation/file-ingestion/javascript-api/compression?v=v2
            if ( params.image.resize.enabled ) {
                var delimiter = 'x';
                for ( var resizekey in params.image.resize ) {
                    if ( resizekey !== 'enabled' && params.image.resize[resizekey].indexOf(delimiter) > -1 ) {
                        var dimensions = params.image.resize[resizekey].split(delimiter);

                        // quick fix
                        dimensions[0] = (!dimensions[0]) ? null : dimensions[0];
                        dimensions[1] = (!dimensions[1]) ? null : dimensions[1];

                        if ( resizekey === 'imageDim' ) {
                            params.pickerOptions[resizekey] = dimensions;
                        } else {
                            // if not imageDim - replace it with max or min if set
                            if ( dimensions[0] || dimensions[1] ) {
                                params.pickerOptions[resizekey] = dimensions;
                                delete params.pickerOptions.imageDim;
                            }
                        }
                    }
                }
            }

            log('Picker options for Image manipulation', params.pickerOptions);
        }

        function hashCode(str){
            var hash = 0;
            if ( Array.prototype.reduce ) {
                hash = str.split("").reduce(function(a,b){a=((a<<5)-a)+b.charCodeAt(0);return a&a},0);
            } else {
                if (str.length === 0) return hash;
                for (var i = 0; i < str.length; i++) {
                    var character  = str.charCodeAt(i);
                    hash = ((hash<<5)-hash)+character;
                    hash = hash & hash;
                }
            }

            return Math.abs(hash);
        }

        /**
         * Append any uploaded files to the form
         * @param e - the object data return by filepicker
         */
        function appendFiles(InkBlob) {
            var urlSplit = String(InkBlob.url).split('/');
            var uniquefilename = String(urlSplit[urlSplit.length - 1]).substr(0,10);
            // var fileHtml = "<a href=\"" + InkBlob.url + "\" title=\"" + InkBlob.filename + "\" target=\"_blank\">" + InkBlob.filename + "</a>";

            var readableFileSize = (typeof InkBlob.size !== 'undefined') ? JotForm.bytesToSize(InkBlob.size, 2) : 'N/A';
            params.uploadedFiles.push({
                key: hashCode(InkBlob.url),
                value: InkBlob.url + ' (' + readableFileSize + ')'
            });

            //set value to hidden element
            $(params.qid).update('').setValue(generateOutput(params.uploadedFiles));

            var li = new Element('li', { 'class': 'qq-upload-success'}).store('inkblob', Object.toJSON(InkBlob));
            var spanFileName = new Element('span', { 'class': 'qq-upload-file', 'id':'qq-upload-file_' + params.qid }).update(InkBlob.filename);
            var spanFileSize = new Element('span', { 'class': 'qq-upload-size', 'id':'qq-upload-size_' + params.qid }).update(readableFileSize);
            var spanFileDelete = new Element('span', { 'class': 'qq-upload-delete', 'id':'qq-upload-delete_' + params.qid }).update("X");

            spanFileDelete.stopObserving().observe("click", function(){
                var $this = this
                  , liParent = $this.up('li.qq-upload-success')
                  , dataInkBlob = liParent.retrieve('inkblob')
                  , cleanInkBlob = dataInkBlob.replace(/\0/g,''); //clean for nulls

                // lets check url bug if crop ui enabled - until filepicker fix it themeselves
                var blob = cleanInkBlob.evalJSON();
                var hashCodekey = hashCode(blob.url);
                log("Removing file " + blob.filename, blob);
                filepicker.remove(blob, function success(){
                    log("Removed " + blob.filename, blob);

                    // remove the uploaded file from cache and update hidden input
                    for ( var index in params.uploadedFiles ) {
                        if ( params.uploadedFiles[index].key === hashCodekey ) {
                            params.uploadedFiles.splice(index, 1);
                            break;
                        }
                    }

                    // update output
                    $(params.qid).update('').setValue(generateOutput(params.uploadedFiles));

                    log("new uploaded files list ", params.uploadedFiles);

                    // remove li element
                    $this.up().remove();
                }, function error(FPError){
                    log('Error removing ' + InkBlob.filename, FPError);
                });
            });

            li.insert(spanFileName);
            li.insert(spanFileSize);
            li.insert(spanFileDelete);

            $("filePickerList_" + params.qid).insert(li);
        }

        /**
         * Handles previous uploaded files
         * when edit mode
         */
        function handlePreviousValuesWhenEditMode() {
            var intervalcount = 500;
            var currentinterval = 0;
            var timeout = 5000; // terminated after 5seconds
            var interval = setInterval(function(){
                var prevVal = $(params.qid).getValue();
                if ( prevVal ) {
                    clearInterval(interval);
                    log('Previous values', prevVal);
                    var prevValArray = prevVal.split(/\r\n|\r|\n/g);
                    if ( prevValArray.length > 0 ) {
                        var rIndex = 0;
                        reqMeta();
                        function reqMeta() {
                            var linkWithSize = prevValArray[rIndex];
                            var link = linkWithSize.split(' ')[0];

                            // get hashcode and register to uploadedFiles variable
                            ajax(link + '/metadata?filename=true&size=true', {
                                method: 'GET',
                                complete: function(response) {
                                    var json = JSON.parse(response);
                                    // console.log('Metadata for ', link, json);
                                    appendFiles({
                                        url: link,
                                        size: json.size,
                                        filename: json.filename
                                    });

                                    rIndex++;
                                    if ( rIndex < prevValArray.length ) {
                                        reqMeta();
                                    } else {
                                        log('Uploaded files updated with previous values', params.uploadedFiles);
                                    }
                                },
                                error: function(e) {
                                    console.error('File picker meta data error for ', link, e);
                                }
                            });
                        }
                    }
                }

                currentinterval += intervalcount;
                if ( currentinterval > timeout ) {
                    clearInterval(interval);
                }
            }, intervalcount);
        }

        /**
         * Generates widget output
         */
        function generateOutput(files) {
            var output = [];
            for ( var g = 0; g < params.uploadedFiles.length; g++ ) {
                output.push(params.uploadedFiles[g].value);
            }
            return output.join('\n');
        }

        /**
         * Handle files from filepicker success function
         * and display it to the form after
         */
        function handleFiles(InkBlob) {
            log("InkBlob response from filepicker API", InkBlob);

            if ( params.multiple ) {
                $A(InkBlob).each(function(e){
                    appendFiles(e);
                });
            } else {
                if ( params.s3.enabled ) {
                    // we expect an array response if uploaded to s3
                    $A(InkBlob).each(function(e){
                        appendFiles(e);
                    });
                } else {
                    appendFiles(InkBlob);
                }
            }
        }

        /**
         * Handle error response from filepicker error function
         */
        function handleError(FPError) {
            log('handleError', FPError.toString());
        }

        /**
         * Upload multiple files to filepicker
         */
        function uploadMultiple() {
            if ( params.s3.enabled ) {
                log("uploader multiple to s3");
                params.pickerOptions.multiple = params.multiple;
                filepicker.pickAndStore(params.pickerOptions, params.pickerOptionsS3, function(InkBlob){
                    handleFiles(InkBlob);
                });
            } else {
                log("uploader multiple");
                filepicker.pickMultiple(params.pickerOptions, function(InkBlob){
                    handleFiles(InkBlob);
                }, function error(err){
                    handleError(err);
                });
            }
        }

        /**
         * Upload a single file to filepicker
         */
        function uploadSingle() {
            if ( params.s3.enabled ) {
                log("uploader single to s3");
                filepicker.pickAndStore(params.pickerOptions, params.pickerOptionsS3, function(InkBlob){
                    handleFiles(InkBlob);
                }, function error(err){
                    handleError(err);
                });
            } else {
                log("uploader single");
                filepicker.pick(params.pickerOptions, function(InkBlob){
                    handleFiles(InkBlob);
                }, function error(err){
                    handleError(err);
                });
            }
        }

        /**
         * Fraction strings to decimal value
         */
        function toDecimal(fraction) {
            if ( fraction.indexOf('/') === -1 ) {
                log('Not a valid fraction');
                return;
            }

            var split = fraction.split('/');
            return parseFloat(split[0]) / parseFloat(split[1]);
        }

        /**
         * Custom log for better debugging
         */
        function log() {
            if ( params.allowDebug && 'console' in window ) {
                console.log.apply(console, arguments);
            }
        }

        /**
         * Native ajax request
         * Prototype.js Ajax is not working quite well
         * with x-origins
         */
        function ajax(url, options) {
            //setting defaults
            url = url || '';
            var method = options.method ? options.method.toUpperCase() : 'POST';
            var success = options.success || function(){};
            var complete = options.complete || function(){};
            var error = options.error || function(){};
            var async = options.async === undefined ? true : options.async;
            var data = options.data || null;
            var finished = false;

            //creating the request
            var xhr;
            if (options.xhr) {
                xhr = options.xhr;
            } else {
                try{
                    // Modern browsers
                    xhr = new window.XMLHttpRequest();
                } catch (e){
                    // IE
                    try{
                        xhr = new window.ActiveXObject('Msxml2.XMLHTTP');
                    } catch (e) {
                        try{
                            xhr = new window.ActiveXObject('Microsoft.XMLHTTP');
                        } catch (e){
                            // Something went wrong
                            xhr = null;
                        }
                    }
                }

                if (!xhr) {
                    options.error('Ajax not allowed');
                    return xhr;
                }
            }

            var finish = function(type,resp,xhr) {
                if (type === 'success') {
                    success(resp, xhr.status, xhr);
                } else if (type === 'error') {
                    error(resp, xhr.status, xhr);
                }
                complete(resp, xhr.status, xhr);
            };

            //Handlers
            var onStateChange = function(){
                if(xhr.readyState == 4 && !finished){
                    if (xhr.status >= 200 && xhr.status < 300) {
                        //TODO - look into using xhr.responseType and xhr.response for binary blobs. Not sure what to return
                        var resp = xhr.responseText;
                        finish('success', resp, xhr);
                        finished = true;
                    } else {
                        onerror.call(xhr, xhr.responseText);
                        finished = true;
                    }
                }
            };
            xhr.onreadystatechange = onStateChange;

            var onerror = function(err) {
                //already handled
                if (finished) {return;}

                finished = true;
                if (this.status == 400) {
                    finish('error', 'bad_params', this);
                    return;
                } else if (this.status == 403) {
                    finish('error', 'not_authorized', this);
                    return;
                } else if (this.status == 404) {
                    finish('error', 'not_found', this);
                    return;
                }

                //if we're here, we don't know what happened
                finish('error', err, this);
            };

            xhr.onerror = onerror;

            //Executing the request
            if (data && method == 'GET') {
                url += (url.indexOf('?') !== -1 ? '&' : '?') + data;
                data = null;
            }

            xhr.open(method, url, async);
            xhr.setRequestHeader('Accept', 'application/json, text/javascript');

            xhr.send(data);

            return xhr;
        }
    }
})();