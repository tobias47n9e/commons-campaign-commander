let $ = require('jquery');
let wdk = require('wikidata-sdk');
let Cookies = require('js-cookie');

/**
* Main class that is used on the campaign commander pages.
*/
class Commander {
    constructor() {
        let wikidataIdField = $('.js-wikidata-id-field');
        let addLanguageButton = $('.js-add-language');
        let submitImageRequest = $('.js-submit-request');
        let optionIcons = $('.js-request-option-icon');
        let coordinateItemInput = $('.js-coordinate-item-input');
        let addImageItem = $('.js-menu-add-image');
        let submitImageButtons = $('.js-submit-image-button');

        this.updateRequestItems();
        wikidataIdField.on('keyup', this.wikidataIdFieldChanged.bind(this));
        addLanguageButton.on('click', this.addLanguage.bind(this));
        submitImageRequest.on('click', this.submitImageForm.bind(this));
        optionIcons.on('click', this.toggleRequestOptions.bind(this));
        coordinateItemInput.on('keyup',
            this.coordinateItemInputChanged.bind(this));
        addImageItem.on('click',
            this.addImageItemClicked.bind(this));
        submitImageButtons.one('click',
            this.submitImageButtonClicked.bind(this));
        this.connectDomEvents();
    }

    /**
    * Connects all the DOM events that need to be called repeatedly
    * to pick up new elements.
    */
    connectDomEvents() {
        let requestLangInput = $('.js-request-text-lang-input');
        let requestTextInput = $('.js-request-text-input');

        requestLangInput.on('keyup', this.requestLangInputChanged.bind(this));
        requestTextInput.on('keyup', this.requestTextInputChanged.bind(this));
    }

    /**
    * Finds all the image-request items on a page and loads
    * the additional data. Duplicate Wikidata IDs are
    * requested only once.
    */
    updateRequestItems() {
        let requestItems = $('.js-request-item');
        let requestMapping = {};
        let self = this;

        for (let item of requestItems) {
            let $item = $(item);

            if ($item.attr('data-request-id') === 'r') {
                let id = $('#wikidata-id-input-r').val().toUpperCase();
                $item.attr('data-wikidata-id', id);
            }

            let requestId = $item.data('request-id');
            let wikidataId = $item.attr('data-wikidata-id');

            if (wikidataId === '') {
                continue;
            }

            if (wikidataId in requestMapping) {
                requestMapping[wikidataId].push(requestId);
            } else {
                requestMapping[wikidataId] = [requestId];
            }
        }

        for (let key in requestMapping) {
            self.fetchItemData(key, requestMapping[key]);
        }
    }

    addImageItemClicked(event) {
        let requestId = $(event.currentTarget).attr('data-request-id');
        let addImageDiv = $('#add-image-div-' + requestId);

        addImageDiv.addClass('show');

    }

    /**
    * Finds all the elements that requrie a Wikidata ID
    * and loads them.
    */
    fetchItemData(wikidataId, requestItems) {
        let wikidataUrl = wdk.getEntities(wikidataId);
        let self = this;

        $.ajax({
            url: wikidataUrl,
            method: 'GET',
            success: function(response) {
                self.setWikidataLabel(response, wikidataId, requestItems);
            },
            error: function(response) {
                console.error(response);
            }
        });
    }

    /**
    * Sets the Wikidata label for a list of requested items.
    * The data of one item (response) is mapped to all the
    * requested-images that are related to that item.
    */
    setWikidataLabel(response, wikidataId, requestItems) {
        let itemLabels = response.entities[wikidataId].labels;

        for (let itemId of requestItems) {
            let selector = '#image-request-' + itemId;
            let $labels = $(selector).find('.js-wikidata-label');

            for (let label of $labels) {
                let $label = $(label);

                let $parent = $label.parents('.js-request-text-item');
                let lang = $parent.find('.js-request-text-lang-input').val();

                if (lang === '' || typeof lang === 'undefined') {
                    lang = $label.attr('data-language');
                }

                let langLabel = itemLabels[lang];
                let labelString;

                if (typeof langLabel === 'undefined') {
                    labelString = 'Label missing';
                } else {
                    labelString = langLabel.value;
                }
                $label.html(labelString);
            }
        }
    }

    /**
    * Used to fetch the coordinates from a Wikidata item.
    */
    setCoordinates(itemId, latitudeField, longitudeField) {
        let itemUrl = wdk.getEntities(itemId);

        $.ajax({
            url: itemUrl,
            method: 'GET',
            success: function(response) {
                if (typeof response.entities === 'undefined') {
                    console.error('Unknown wikidata ID');
                }

                let claims = response.entities[itemId].claims;

                if ('P625' in claims) {
                    let value = claims['P625'][0].mainsnak.datavalue.value;
                    latitudeField.val(value.latitude);
                    longitudeField.val(value.longitude);
                } else {
                    latitudeField.val('');
                    longitudeField.val('');
                }
            },
            error: function(response) {
                console.error(response);
            }
        });
    }

    /**
    * Triggered by the Wikidata ID field being changed (keyup).
    * Calls a function to get the coordinates.
    * Sets the Wikidata ID for the labels.
    * Find the labels.
    */
    wikidataIdFieldChanged(event) {
        let eventField = $(event.currentTarget);
        let requestId = eventField.data('request-id');
        let requestItem = $('#image-request-r');
        let latitudeField = requestItem.find('.js-latitude-field');
        let longitudeField = requestItem.find('.js-longitude-field');
        let wikidataLabels = requestItem.find('.js-wikidata-label');
        let itemId = eventField.val();

        if (itemId.length > 0) {
            if (itemId.slice(0,1).toUpperCase() === 'Q') {
                itemId = itemId.slice(1);
            }

            if (parseInt(itemId)) {
                itemId = 'Q' + itemId;
                this.setCoordinates(itemId, latitudeField,
                                    longitudeField);
                wikidataLabels.attr('data-wikidata-id', itemId);
                requestItem.attr('data-wikidata-id', itemId);
                this.updateRequestItems();
            }
        }
    }

    /**
    * Tries to validate the Wikidata ID
    */
    cleanWikidataId(wikidataId) {
        let cleanId = false;

        if (wikidataId.length > 0) {
            if (wikidataId.slice(0,1).toUpperCase() === 'Q') {
                wikidataId = wikidataId.slice(1);
            }

            if (parseInt(wikidataId)) {
                cleanId = 'Q' + wikidataId;
            }
        }

        return cleanId;
    }

    /**
    * Sets the coordinates using a wikidata-id and the two
    * fields for the coordinates.
    */
    setCoordinatesNew(wikidataId, latitudeField, longitudeField, inputField) {
        let wikidataUrl = wdk.getEntities(wikidataId);

        function setValues(response) {
            if (typeof response.entities === 'undefined') {
                console.error('Unknown wikidata ID');
                inputField.addClass('invalid');
                return
            }

            let claims = response.entities[wikidataId].claims;

            if (typeof claims === 'undefined') {
                inputField.addClass('invalid');
                return
            }

            if ('P625' in claims) {
                let value = claims['P625'][0].mainsnak.datavalue.value;
                latitudeField.val(value.latitude);
                longitudeField.val(value.longitude);
            } else {
                inputField.addClass('invalid');
                latitudeField.val('');
                longitudeField.val('');
            }
        }

        $.ajax({
            url: wikidataUrl,
            method: 'GET',
            success: function(response) {
                setValues(response);
            },
            error: function(response) {
                console.error(response);
            }
        });
    }

    /**
    * When the input field for the coordinate item is changed
    * the coordinates are inserted into the coordinate field.
    */
    coordinateItemInputChanged(event) {
        let inputField = $(event.currentTarget);
        let wikidataId = inputField.val();
        let requestId = inputField.attr('data-request-id');
        let latitudeField = $('#latitude-input-' + requestId);
        let longitudeField = $('#longitude-input-' + requestId);
        inputField.removeClass('invalid');

        if (wikidataId === '') {
            return
        }

        wikidataId = this.cleanWikidataId(wikidataId);

        if (wikidataId == false) {
            inputField.addClass('invalid');
        }

        if (wikidataId !== '') {
            this.setCoordinatesNew(wikidataId, latitudeField,
                                longitudeField, inputField);
        }
    }

    /**
    * Adds another language row to a request item.
    */
    addLanguage(event) {
        event.preventDefault();
        let addButton = $(event.currentTarget);
        let requestItem = addButton.parents('.js-request-item');
        let firstRequestText = requestItem.find('.js-first-request-item');
        let moreRequests = requestItem.find('.js-more-request-rows');
        moreRequests.append(firstRequestText.html());
        this.connectDomEvents();
    }

    /**
    * Triggered when the language is changed in a row
    * containing the request text. Updates the text area that
    * is associated with the language field.
    */
    requestLangInputChanged(event) {
        let langInput = $(event.currentTarget);
        let requestItem = langInput.parents('.js-request-text-item');
        let requestTextInput = requestItem.find('.js-request-text-input');
        let wikidataLabel = requestItem.find('.js-wikidata-label');
        langInput.removeClass('invalid');

        if (langInput.val() === '') {
            langInput.addClass('invalid');
        }

        requestTextInput.attr('name', 'text_' + langInput.val());
        langInput.attr('name', 'lang_' + langInput.val());
        wikidataLabel.attr('data-language', langInput.val());
        this.updateRequestItems();
    }

    /**
    * Validates and submits the requested image form.
    */
    submitImageForm(event) {
        event.preventDefault();
        let formButton = $(event.currentTarget);
        let requestItem = formButton.parents('.js-request-item');
        let requestForm = requestItem.find('.js-request-form');
        let csrftoken = Cookies.get('csrftoken');
        let self = this;

        let formValid = this.validateForm(requestItem);
        let data = requestForm.serializeArray();
        let cleanedData = this.cleanImageRequestData(data);

        formButton.addClass('loading');

        $.ajax({
            url: '/api/image-requests',
            method: 'POST',
            beforeSend: function(xhr, settings) {
                if (!self.csrfSafeMethod(settings.type) && !this.crossDomain) {
                    xhr.setRequestHeader("X-CSRFToken", csrftoken);
                }
            },
            dataType: "json",
            contentType: 'application/json',
            data: cleanedData,
            success: function(response) {
                formButton.removeClass('loading');
                window.location = '/add-image-request'
            },
            error: function(response) {
                console.error(response);
            }
        });
    }

    /**
    * Gets the raw image request form data and returns
    * a structured JSON file that can be submitted.
    */
    cleanImageRequestData(formData) {
        let formJson = {
            request_texts: [],
            submitted_images: []
        };
        let latitude, longitude;

        for (let i = 0; i < formData.length; i++) {
            let name = formData[i].name;
            let value = formData[i].value;

            let type = name.split('_')[0];
            let lang = name.split('_')[1];

            if (name === 'latitude') {
                latitude = value;
                continue;
            }

            if (name === 'longitude') {
                longitude = value;
                continue;
            }

            if (type === 'text') {
                let requestText = {
                    lang: lang,
                    text: value
                };
                formJson.request_texts.push(requestText);
            } else if (type === 'lang') {
                continue;
            } else {
                formJson[name] = value;
            }
        }

        let points = 'MULTIPOINT((' + longitude + ' ' + latitude + '))';
        formJson.points = points;

        formJson = JSON.stringify(formJson);
        return formJson;
    }

    /**
    * Puts an image request item into submit image mode.
    */
    requestTextInputChanged(event) {
        let requestTextInput = $(event.currentTarget);
        requestTextInput.removeClass('invalid');

        if (requestTextInput.val() === '') {
            requestTextInput.addClass('invalid');
        }
    }

    /**
    * Handles the submitting of an image in an image request item.
    */
    submitImageButtonClicked(event) {
        event.preventDefault();
        let self = this;
        let csrftoken = Cookies.get('csrftoken');
        let submitImageButton = $(event.currentTarget);
        let imageRequestId = submitImageButton.attr('data-request-id');
        let submitImageForm = $('#submit-image-form-' + imageRequestId);

        let data = submitImageForm.serializeArray();
        let cleanedData = {};

        for (let item of data) {
            cleanedData[item.name] = item.value;
        }

        let jsonString = JSON.stringify(cleanedData);

        $.ajax({
            url: '/api/submitted-images',
            method: 'POST',
            beforeSend: function(xhr, settings) {
                if (!self.csrfSafeMethod(settings.type) && !this.crossDomain) {
                    xhr.setRequestHeader("X-CSRFToken", csrftoken);
                }
            },
            dataType: "json",
            contentType: 'application/json',
            data: jsonString,
            success: function(response) {
                console.log('submit success');
                console.log(response);
                window.location = '/image-requests'
            },
            error: function(response) {
                console.error(response);
            }
        });
    }

    /**
    * Validates a image request item form.
    */
    validateForm(requestItem) {
        let isValid = true;
        let $languageFields = requestItem.find(`.js-request-text-lang-input,
                                .js-request-text-input`);
        let $wikidataIdField = $('#wikidata-id-input-r');

        for (let field of $languageFields) {
            let $field = $(field);

            if ($field.val() === '') {
                $field.addClass('invalid');
            }
        }

        let idValue = $wikidataIdField.val();

        if (idValue === '') {
            $wikidataIdField.addClass('invalid')
        } else {
            if (idValue.slice(0, 1).toUpperCase() !== 'Q') {
                $wikidataIdField.addClass('invalid')
            }
        }

        return isValid;
    }

    /**
    * Returns all methods that don't need CSRF protection.
    */
    csrfSafeMethod(method) {
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }

    toggleRequestOptions(event) {
        let $icon = $(event.currentTarget);
        let requestId = $icon.data('request-id');
        let $menu = $('#request-option-menu-' + requestId);
        $menu.toggleClass('show');
    }
}

let commander = new Commander();
