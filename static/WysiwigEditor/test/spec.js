describe('testpage', function() {
    it('should have a title', function() {
        browser.get('http://localhost/HEIDIEditor/html/test.html');

        expect(browser.getTitle()).toEqual('Book Metadata | HEIDIEditor');
    });
});