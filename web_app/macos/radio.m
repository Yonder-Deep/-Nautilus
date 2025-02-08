#import <Foundation/Foundation.h>
#import <IOKit/IOTypes.h>
#import <IOKit/IOKitKeys.h>
#import <IOKit/usb/IOUSBLib.h>
#import <IOKit/IOBSD.h>
#import <sys/param.h>
#import <paths.h>

char* find_radio() {
    NSLog(@"Finding path to radio device...");

    // Create subdictionary key-pair to match radio USB UART
    CFMutableDictionaryRef subDict;
    subDict = CFDictionaryCreateMutable(kCFAllocatorDefault, 0,
            &kCFTypeDictionaryKeyCallBacks,
            &kCFTypeDictionaryValueCallBacks);
    CFDictionarySetValue(subDict, CFSTR("kUSBProductString"),
            CFSTR("FT231X USB UART"));

    // Add to matching dictionary w/ catch-all "kIOPropertyMatchKey"
    CFMutableDictionaryRef matchingUSBDict;
    matchingUSBDict = CFDictionaryCreateMutable(kCFAllocatorDefault, 0,
            &kCFTypeDictionaryKeyCallBacks,
            &kCFTypeDictionaryValueCallBacks);
    CFDictionarySetValue(matchingUSBDict, CFSTR(kIOPropertyMatchKey),
            subDict);
    
    NSLog(@"Matching Dict:");
    NSLog(@"%@", matchingUSBDict);

    // Find the first service in the I/O Registry that matches our dictionary
    io_service_t matchedService;
    matchedService = IOServiceGetMatchingService(kIOMainPortDefault, matchingUSBDict);

    NSLog(@"Service: %u", matchedService);
    
    // Service path, not really that useful for our purposes
    io_string_t servicePath;
    IORegistryEntryGetPath(matchedService, kIOServicePlane, servicePath);
    NSLog(@"Service Path: %s", servicePath);
    NSLog(@"USB Path: %d", IORegistryEntryGetPath(matchedService, kIOPowerPlane, servicePath));

    // This is the [BSDName] appended to the filepath: /dev/tty.usbserial-[BSDName]
    CFStringRef deviceBSDName_cf = (CFStringRef) IORegistryEntrySearchCFProperty(
            matchedService,
            kIOServicePlane,
            CFSTR (kUSBSerialNumberString),
            kCFAllocatorDefault,
            kIORegistryIterateRecursively );
    NSLog(@"BSD Name: %@", deviceBSDName_cf);

    char deviceFilePath[MAXPATHLEN]; // MAXPATHLEN is defined in sys/param.h
    size_t devPathLength;
    Boolean gotString = false;

    /* This commented part is from the Apple docs but always comes up null    
    CFTypeRef deviceNameAsCFString;
    deviceNameAsCFString = (CFStringRef) IORegistryEntrySearchCFProperty (
            matchedService,
            kIOServicePlane,
            CFSTR(kIOBSDNameKey),
            kCFAllocatorDefault,
            kIORegistryIterateRecursively);
    NSLog(@"hi");
    NSLog(@"%@", deviceNameAsCFString);*/
    if (deviceBSDName_cf) {
        NSLog(@"BSDName found, finding path...");
        char deviceFilePath[MAXPATHLEN];
        devPathLength = strlen(_PATH_DEV); //_PATH_DEV defined in paths.h
        strcpy(deviceFilePath, _PATH_DEV);
        strcat(deviceFilePath, "tty.usbserial-");
        gotString = CFStringGetCString(deviceBSDName_cf,
                deviceFilePath + strlen(deviceFilePath),
                MAXPATHLEN - strlen(deviceFilePath),
                kCFStringEncodingASCII);
        
        if (gotString) {
            NSLog(@"Device file path: %s", deviceFilePath);
            char* finalResult = malloc(strlen(deviceFilePath));
            strcpy(finalResult, deviceFilePath);
            return finalResult;
        } else {
            NSLog(@"Radio device not found.");
        }
    } else {
        NSLog(@"Radio device not found.");
    }
    char* notFound = malloc(21);
    strcpy(notFound, "Radio device not found");
    return notFound;
}

int main() {
    char* result = find_radio();
    NSLog(@"Result: %s", result);
    free(result);
    return 0;
}